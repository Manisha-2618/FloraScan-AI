"""
app.py - Main Flask Application for Plant Disease Detection.
Provides web UI routes, REST API endpoints, image upload handling,
and integrates the Machine Learning classification pipeline.
"""

import logging
import os
import threading
import uuid
from pathlib import Path
from typing import Any
# Flask core web framework imports
from flask import (
    Flask,
    jsonify,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
)
from PIL import Image, UnidentifiedImageError
from werkzeug.utils import secure_filename

# Local prediction and training imports
from predict import (
    DEFAULT_CLASS_NAMES_PATH,
    DEFAULT_MODEL_PATH,
    load_class_names,
    load_model,
    predict_image,
)
from train import train_pipeline

# Configure application logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("PlantDiseaseApp")

# Application base paths
BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
MODEL_DIR = BASE_DIR / "model"
DATASET_DIR = BASE_DIR / "dataset"
STATIC_DIR = BASE_DIR / "static"
TEMPLATES_DIR = BASE_DIR / "templates"

# Ensure essential runtime folders exist
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
MODEL_DIR.mkdir(parents=True, exist_ok=True)

# Allowed file formats
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 Megabytes

# Initialize Flask application
app = Flask(
    __name__,
    template_folder=str(TEMPLATES_DIR),
    static_folder=str(STATIC_DIR)
)
app.config["UPLOAD_FOLDER"] = str(UPLOAD_DIR)
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH
app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY", "plant-disease-secret-key-2026")

# Global ML model and class cache
app_model = None
app_class_names = None
model_load_error = None


def init_ml_model():
    """Attempts to initialize the ML model and class names on startup."""
    global app_model, app_class_names, model_load_error
    try:
        if DEFAULT_MODEL_PATH.exists() and DEFAULT_CLASS_NAMES_PATH.exists():
            app_model = load_model(DEFAULT_MODEL_PATH)
            app_class_names = load_class_names(DEFAULT_CLASS_NAMES_PATH)
            model_load_error = None
            logger.info(f"ML Model loaded successfully with {len(app_class_names)} classes.")
        else:
            model_load_error = (
                "Model files are not found. Please train the model by running 'python train.py' "
                "or using the Model Training dashboard."
            )
            logger.warning(model_load_error)
    except Exception as e:
        model_load_error = f"Error loading model: {str(e)}"
        logger.error(model_load_error, exc_info=True)


# Perform model check on app launch
init_ml_model()


def allowed_file(filename: str | None) -> bool:
    """Verifies that a filename contains one of the permitted extensions."""
    if not filename:
        return False
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def get_dataset_stats() -> dict:
    """Inspects the dataset directory and returns class counts and image totals."""
    stats = {
        "train_classes": [],
        "train_image_count": 0,
        "val_image_count": 0,
        "has_dataset": False
    }
    train_dir = DATASET_DIR / "train"
    val_dir = DATASET_DIR / "validation"

    valid_exts = {".jpg", ".jpeg", ".png", ".webp"}

    if train_dir.exists() and train_dir.is_dir():
        for folder in sorted(train_dir.iterdir()):
            if folder.is_dir() and not folder.name.startswith("."):
                img_files = [f for f in folder.iterdir() if f.is_file() and f.suffix.lower() in valid_exts]
                if img_files:
                    stats["train_classes"].append({
                        "name": folder.name,
                        "count": len(img_files)
                    })
                    stats["train_image_count"] += len(img_files)

    if val_dir.exists() and val_dir.is_dir():
        for folder in sorted(val_dir.iterdir()):
            if folder.is_dir() and not folder.name.startswith("."):
                img_files = [f for f in folder.iterdir() if f.is_file() and f.suffix.lower() in valid_exts]
                stats["val_image_count"] += len(img_files)

    stats["has_dataset"] = len(stats["train_classes"]) > 0
    return stats


# -----------------------------------------------------------------------------
# Background Training State Management
# -----------------------------------------------------------------------------
training_state: dict[str, Any] = {
    "is_running": False,
    "status": "idle",
    "progress": 0,
    "current_epoch": 0,
    "total_epochs": 0,
    "latest_metrics": {},
    "logs": [],
    "error": None
}
training_lock = threading.Lock()


def run_training_worker(epochs: int, batch_size: int):
    """Worker thread that executes train_pipeline safely in the background."""
    global training_state, app_model, app_class_names, model_load_error

    with training_lock:
        training_state["is_running"] = True
        training_state["status"] = "running"
        training_state["progress"] = 0
        training_state["current_epoch"] = 0
        training_state["total_epochs"] = epochs
        training_state["logs"] = [f"Starting training run ({epochs} epochs, batch size {batch_size})..."]
        training_state["error"] = None

    def on_epoch_end(epoch, total_epochs, logs):
        with training_lock:
            training_state["current_epoch"] = epoch
            training_state["progress"] = int((epoch / total_epochs) * 100)
            clean_logs = {k: round(float(v), 4) for k, v in (logs or {}).items()}
            training_state["latest_metrics"] = clean_logs
            training_state["logs"].append(
                f"Epoch {epoch}/{total_epochs} completed - Loss: {clean_logs.get('loss', 'N/A')}, "
                f"Accuracy: {clean_logs.get('accuracy', 'N/A')}, "
                f"Val Loss: {clean_logs.get('val_loss', 'N/A')}, "
                f"Val Accuracy: {clean_logs.get('val_accuracy', 'N/A')}"
            )

    try:
        result = train_pipeline(
            data_dir_path=str(DATASET_DIR),
            model_dir_path=str(MODEL_DIR),
            epochs=epochs,
            batch_size=batch_size,
            progress_callback=on_epoch_end
        )
        with training_lock:
            training_state["is_running"] = False
            training_state["status"] = "completed"
            training_state["progress"] = 100
            training_state["logs"].append("Training successfully finished and model weights saved!")
            training_state["latest_metrics"] = result

        # Reload newly trained model into memory
        init_ml_model()

    except Exception as e:
        logger.error(f"Background training failed: {e}", exc_info=True)
        with training_lock:
            training_state["is_running"] = False
            training_state["status"] = "failed"
            training_state["error"] = str(e)
            training_state["logs"].append(f"Training failed with error: {e}")


# -----------------------------------------------------------------------------
# Web Page Routes (HTML Templates)
# -----------------------------------------------------------------------------

@app.route("/", methods=["GET"])
def index():
    """Renders the main plant leaf diagnostic interface."""
    model_available = (app_model is not None and app_class_names is not None)
    class_count = len(app_class_names) if app_class_names else 0
    return render_template(
        "index.html",
        model_loaded=model_available,
        class_count=class_count,
        model_error=model_load_error
    )


@app.route("/about", methods=["GET"])
def about():
    """Renders the project documentation and methodology page."""
    return render_template("about.html")


@app.route("/train", methods=["GET"])
def train():
    """Renders the model training control center and dataset overview."""
    stats = get_dataset_stats()
    model_available = (app_model is not None and app_class_names is not None)
    model_file_exists = DEFAULT_MODEL_PATH.exists()
    model_size_mb = round(DEFAULT_MODEL_PATH.stat().st_size / (1024 * 1024), 2) if model_file_exists else 0

    return render_template(
        "train.html",
        stats=stats,
        model_loaded=model_available,
        model_file_exists=model_file_exists,
        model_size_mb=model_size_mb,
        class_names=app_class_names or [],
        training_state=training_state
    )


@app.route("/predict", methods=["POST"])
def predict():
    """
    Standard HTML Form POST handler:
    Accepts an uploaded image, runs prediction, and renders result.html.
    """
    global app_model, app_class_names

    # Check model readiness
    if app_model is None or app_class_names is None:
        init_ml_model()
        if app_model is None or app_class_names is None:
            return render_template(
                "result.html",
                error="Model is not ready. Please train the model using 'python train.py' or the Model Training page.",
                success=False
            ), 503

    # Validate file presence
    if "image" not in request.files:
        return render_template("result.html", error="No image file provided in form submission.", success=False), 400

    file = request.files["image"]
    if not file.filename:
        return render_template("result.html", error="No image selected for upload.", success=False), 400

    if not allowed_file(file.filename):
        return render_template(
            "result.html",
            error=f"Unsupported file format. Please upload one of: {', '.join(sorted(ALLOWED_EXTENSIONS)).upper()}",
            success=False
        ), 400

    # Secure filename and save
    original_name = secure_filename(file.filename)
    extension = original_name.rsplit(".", 1)[1].lower() if "." in original_name else "jpg"
    unique_filename = f"leaf_{uuid.uuid4().hex[:10]}.{extension}"
    save_path = UPLOAD_DIR / unique_filename

    try:
        file.save(str(save_path))

        # Validate that the file is indeed an authentic decodable image
        with Image.open(str(save_path)) as img:
            img.verify()

        # Run prediction pipeline
        prediction = predict_image(save_path, model=app_model, class_names=app_class_names)
        image_url = url_for("uploaded_file", filename=unique_filename)

        return render_template(
            "result.html",
            success=True,
            image_url=image_url,
            plant=prediction["plant"],
            disease=prediction["disease"],
            confidence=prediction["confidence"],
            description=prediction["description"],
            symptoms=prediction["symptoms"],
            treatment=prediction["treatment"],
            disclaimer=prediction.get("disclaimer", ""),
            top_predictions=prediction.get("top_predictions", [])
        )

    except UnidentifiedImageError:
        if save_path.exists():
            save_path.unlink()
        return render_template("result.html", error="Uploaded file is corrupted or not a valid image.", success=False), 400

    except Exception as e:
        logger.error(f"Prediction error during form POST: {e}", exc_info=True)
        return render_template("result.html", error=f"An error occurred during image diagnosis: {str(e)}", success=False), 500


# -----------------------------------------------------------------------------
# RESTful API Endpoints (JSON / Fetch API)
# -----------------------------------------------------------------------------

@app.route("/api/predict", methods=["POST"])
def api_predict():
    """
    REST API endpoint for image disease classification.
    Accepts multipart/form-data with 'image' field.
    Returns JSON structured diagnosis response.
    """
    global app_model, app_class_names

    # Check model readiness
    if app_model is None or app_class_names is None:
        init_ml_model()
        if app_model is None or app_class_names is None:
            return jsonify({
                "success": False,
                "error": "The Machine Learning model is not loaded. Train the model using 'python train.py' or through the training dashboard."
            }), 503

    # Check file input
    if "image" not in request.files:
        return jsonify({"success": False, "error": "No 'image' field found in multipart form data."}), 400

    file = request.files["image"]
    if not file.filename:
        return jsonify({"success": False, "error": "No file was selected for upload."}), 400

    if not allowed_file(file.filename):
        return jsonify({
            "success": False,
            "error": f"Invalid file format. Allowed extensions: {', '.join(sorted(ALLOWED_EXTENSIONS)).upper()}"
        }), 400

    # Save image with collision-proof secure name
    orig_name = secure_filename(file.filename)
    ext = orig_name.rsplit(".", 1)[1].lower() if "." in orig_name else "jpg"
    unique_name = f"leaf_{uuid.uuid4().hex[:10]}.{ext}"
    save_path = UPLOAD_DIR / unique_name

    try:
        file.save(str(save_path))

        # Validate image file integrity
        with Image.open(str(save_path)) as img:
            img.verify()

        # Run prediction
        result = predict_image(save_path, model=app_model, class_names=app_class_names)
        image_url = url_for("uploaded_file", filename=unique_name)

        return jsonify({
            "success": True,
            "plant": result["plant"],
            "disease": result["disease"],
            "confidence": result["confidence"],
            "description": result["description"],
            "symptoms": result["symptoms"],
            "treatment": result["treatment"],
            "disclaimer": result.get("disclaimer", ""),
            "top_predictions": result.get("top_predictions", []),
            "image_url": image_url
        }), 200

    except UnidentifiedImageError:
        if save_path.exists():
            save_path.unlink()
        return jsonify({"success": False, "error": "The uploaded file is not a valid or readable image."}), 400

    except Exception as e:
        logger.error(f"API prediction error: {e}", exc_info=True)
        return jsonify({"success": False, "error": f"Diagnostic prediction failed: {str(e)}"}), 500


@app.route("/api/health", methods=["GET"])
def api_health():
    """Health check endpoint indicating server and model readiness."""
    model_status = (app_model is not None and app_class_names is not None)
    return jsonify({
        "status": "ok",
        "model_loaded": model_status,
        "classes_count": len(app_class_names) if app_class_names else 0,
        "uptime": "operational"
    }), 200


@app.route("/api/dataset/info", methods=["GET"])
def api_dataset_info():
    """Returns dataset summary and class distribution."""
    stats = get_dataset_stats()
    return jsonify({"success": True, "data": stats}), 200


@app.route("/api/train", methods=["POST"])
def api_start_training():
    """Launches model training asynchronously in a dedicated worker thread."""
    global training_state

    with training_lock:
        if training_state["is_running"]:
            return jsonify({
                "success": False,
                "error": "A training session is already in progress. Please wait for it to complete."
            }), 409

    data = request.get_json(silent=True) or {}
    epochs = int(data.get("epochs", 5))
    batch_size = int(data.get("batch_size", 16))

    # Clamp ranges safely
    epochs = max(1, min(epochs, 50))
    batch_size = max(4, min(batch_size, 64))

    worker = threading.Thread(
        target=run_training_worker,
        args=(epochs, batch_size),
        daemon=True
    )
    worker.start()

    return jsonify({
        "success": True,
        "message": f"Training process dispatched for {epochs} epoch(s).",
        "epochs": epochs,
        "batch_size": batch_size
    }), 202


@app.route("/api/train/status", methods=["GET"])
def api_training_status():
    """Returns real-time progress and logs of background training."""
    with training_lock:
        state_copy = dict(training_state)
    return jsonify(state_copy), 200


@app.route("/uploads/<filename>", methods=["GET"])
def uploaded_file(filename: str):
    """Serves uploaded user leaf images from the uploads directory."""
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


# -----------------------------------------------------------------------------
# Global Error Handlers
# -----------------------------------------------------------------------------

@app.errorhandler(413)
def request_entity_too_large(error):
    """Handles file uploads exceeding max allowable payload."""
    if request.path.startswith("/api/"):
        return jsonify({"success": False, "error": "File size exceeds the 16MB upload limit."}), 413
    return render_template("result.html", error="File size exceeds the 16MB limit.", success=False), 413


@app.errorhandler(404)
def not_found_error(error):
    """Handles 404 Not Found."""
    if request.path.startswith("/api/"):
        return jsonify({"success": False, "error": "Endpoint not found."}), 404
    return redirect(url_for("index"))


@app.errorhandler(500)
def internal_error(error):
    """Handles 500 Internal Server Errors gracefully."""
    logger.error(f"Internal server error: {error}")
    if request.path.startswith("/api/"):
        return jsonify({"success": False, "error": "An internal server error occurred."}), 500
    return render_template("result.html", error="An internal server error occurred.", success=False), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug_mode = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    logger.info(f"Starting Plant Disease Detection Flask Server on http://127.0.0.1:{port}")
    app.run(host="0.0.0.0", port=port, debug=debug_mode)
