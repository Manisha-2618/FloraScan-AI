"""
predict.py - Reusable image prediction pipeline for Plant Disease Detection.
Handles image loading, preprocessing, model inference, and class mapping.
"""

import json
import logging
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

import numpy as np
from PIL import Image

# Import disease info and fallbacks
from disease_info import get_disease_details

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Base paths
PROJECT_ROOT = Path(__file__).resolve().parent
MODEL_DIR = PROJECT_ROOT / "model"
DEFAULT_MODEL_PATH = MODEL_DIR / "plant_disease_model.keras"
DEFAULT_CLASS_NAMES_PATH = MODEL_DIR / "class_names.json"

# Global cache for loaded model and class names
_CACHED_MODEL = None
_CACHED_CLASS_NAMES = None


def load_model(model_path: Optional[Union[str, Path]] = None):
    """
    Loads and caches the trained Keras model.
    Returns the loaded model instance.
    Raises FileNotFoundError if model file does not exist.
    """
    global _CACHED_MODEL
    
    if _CACHED_MODEL is not None and model_path is None:
        return _CACHED_MODEL

    target_path = Path(model_path) if model_path else DEFAULT_MODEL_PATH
    
    if not target_path.exists():
        raise FileNotFoundError(
            f"Model file not found at '{target_path}'. "
            "Please train the model first by running 'python train.py' or via the training dashboard."
        )

    logger.info(f"Loading trained Keras model from {target_path}...")
    import tensorflow as tf
    try:
        model = tf.keras.models.load_model(str(target_path))
    except Exception as err:
        logger.warning(f"Standard load failed ({err}), retrying with safe_mode=False...")
        model = tf.keras.models.load_model(str(target_path), safe_mode=False)
    logger.info("Model loaded successfully.")
    _CACHED_MODEL = model
    return model


def load_class_names(class_names_path: Optional[Union[str, Path]] = None) -> List[str]:
    """
    Loads and caches the list of class names from JSON.
    Returns list of strings.
    Raises FileNotFoundError if JSON is missing.
    """
    global _CACHED_CLASS_NAMES
    
    if _CACHED_CLASS_NAMES is not None and class_names_path is None:
        return _CACHED_CLASS_NAMES

    target_path = Path(class_names_path) if class_names_path else DEFAULT_CLASS_NAMES_PATH
    
    if not target_path.exists():
        raise FileNotFoundError(
            f"Class names file not found at '{target_path}'. "
            "Please train the model first by running 'python train.py' or provide class_names.json."
        )

    with open(target_path, "r", encoding="utf-8") as f:
        class_names = json.load(f)

    if not isinstance(class_names, list) or len(class_names) == 0:
        raise ValueError(f"Invalid class names format in '{target_path}'. Expected non-empty list.")

    _CACHED_CLASS_NAMES = class_names
    return class_names


def preprocess_image(
    image_input: Union[str, Path, Image.Image, Any],
    target_size: Tuple[int, int] = (224, 224)
) -> np.ndarray:
    """
    Loads and preprocesses an image for inference:
    1. Opens image from path, stream, or PIL object
    2. Converts to RGB (handles RGBA, Grayscale, etc.)
    3. Resizes to target_size (default 224x224)
    4. Converts to float32 NumPy array
    5. Applies MobileNetV2 preprocessing (scales pixel values between -1 and 1)
    6. Expands dimensions to batch shape (1, height, width, 3)
    """
    import tensorflow as tf
    from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

    # Step 1: Obtain PIL Image
    if isinstance(image_input, Image.Image):
        img = image_input
    elif isinstance(image_input, (str, Path)):
        img = Image.open(str(image_input))
    else:
        # File-like object (e.g. Flask FileStorage.stream)
        img = Image.open(image_input)

    # Step 2: Ensure 3-channel RGB format
    if img.mode != "RGB":
        img = img.convert("RGB")

    # Step 3: Resize with high-quality resampling
    img = img.resize(target_size, Image.Resampling.BILINEAR)

    # Step 4: Convert to NumPy array
    img_array = np.array(img, dtype=np.float32)

    # Step 5: MobileNetV2 preprocessing (maps [0, 255] to [-1, 1])
    img_preprocessed = preprocess_input(img_array)

    # Step 6: Expand batch dimension
    img_batch = np.expand_dims(img_preprocessed, axis=0)

    return img_batch


def predict_image(
    image_input: Union[str, Path, Image.Image, Any],
    model: Optional[Any] = None,
    class_names: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    End-to-end prediction function:
    1. Preprocesses the image
    2. Executes inference with the ML model
    3. Identifies highest-probability class and confidence score
    4. Gathers top 3 predictions
    5. Retrieves botanical disease information (symptoms, treatment, description)
    6. Returns structured prediction dictionary
    """
    # Ensure model and class names are available
    if model is None:
        model = load_model()
    if class_names is None:
        class_names = load_class_names()

    # Preprocess image
    preprocessed_array = preprocess_image(image_input, target_size=(224, 224))

    # Run inference
    predictions = model.predict(preprocessed_array, verbose=0)
    probabilities = predictions[0]

    # Highest probability prediction
    top_index = int(np.argmax(probabilities))
    confidence = float(probabilities[top_index]) * 100.0
    predicted_class = class_names[top_index]

    # Gather top-k predictions for transparency
    top_k_indices = np.argsort(probabilities)[::-1][:min(3, len(class_names))]
    top_predictions = []
    for idx in top_k_indices:
        top_predictions.append({
            "class_name": class_names[idx],
            "confidence": round(float(probabilities[idx]) * 100.0, 2)
        })

    # Retrieve comprehensive botanical and treatment details
    details = get_disease_details(predicted_class)

    return {
        "success": True,
        "class_name": predicted_class,
        "plant": details["plant"],
        "disease": details["disease"],
        "confidence": round(confidence, 2),
        "description": details["description"],
        "symptoms": details["symptoms"],
        "treatment": details["treatment"],
        "disclaimer": details.get("disclaimer", ""),
        "top_predictions": top_predictions
    }


if __name__ == "__main__":
    import sys
    print("Plant Disease Prediction Pipeline Test")
    print(f"Default model path: {DEFAULT_MODEL_PATH}")
    print(f"Default class names path: {DEFAULT_CLASS_NAMES_PATH}")
    if DEFAULT_MODEL_PATH.exists() and DEFAULT_CLASS_NAMES_PATH.exists():
        print("Model and class names detected. Ready for inference.")
    else:
        print("Model has not been trained yet. Run 'python train.py' to generate model.")
