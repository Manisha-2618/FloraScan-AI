# 🌿 FloraScan AI — Plant Disease Detection System

A complete, end-to-end Machine Learning web application for diagnosing foliar plant diseases using **Python Flask**, **TensorFlow / Keras (MobileNetV2)**, **HTML5**, **Vanilla CSS3**, and **JavaScript Fetch API**.

![FloraScan AI Logo](static/images/logo.png)

---

## 🌟 Key Features

- **Leaf Image Upload:** Drag-and-drop or browse plant leaf images (PNG, JPG, JPEG, WEBP up to 16MB).
- **Deep Learning Inference:** Transfer Learning using MobileNetV2 pretrained on ImageNet for fast and accurate classification.
- **Dynamic Diagnosis UI:**
  - Crop & Disease Identification
  - Confidence Percentage & Visual Confidence Meter
  - Detailed Pathology Overview & Description
  - Observed Symptoms Checklist
  - Actionable Management & Prevention Steps
  - Top Alternative Candidate Predictions
- **Dual Processing Paths:**
  - Interactive AJAX / Fetch API with dynamic DOM rendering without page reloads.
  - Standard HTML form submission rendering dedicated `result.html`.
- **Model Training Dashboard (`/train`):**
  - Dataset overview and class distribution metrics.
  - One-click asynchronous web-based training with live progress and console logs.
  - Standalone CLI training with `python train.py`.
- **Safe Fallback & Error Handling:**
  - Graceful handling of corrupted images, missing files, or missing models.
  - Informative educational disclaimer regarding agricultural treatments.

---

## 📁 Project Structure

```text
PlantDiseaseProject/
│
├── app.py                     # Main Flask web server & REST API
├── train.py                   # Standalone MobileNetV2 CNN training script
├── predict.py                 # Modular image preprocessing & inference pipeline
├── disease_info.py            # Comprehensive disease catalog & dynamic fallback
├── setup_starter_dataset.py   # Starter dataset generator & asset setup
├── requirements.txt           # Python dependency requirements
├── README.md                  # Complete project documentation
├── .gitignore                 # Git ignore rules
│
├── model/
│   ├── plant_disease_model.keras   # Saved trained Keras model weights
│   └── class_names.json            # Target disease class labels list
│
├── dataset/
│   ├── train/                 # Training dataset organized by class subfolders
│   │   ├── Apple___Apple_scab/
│   │   ├── Apple___Black_rot/
│   │   ├── Apple___healthy/
│   │   ├── Tomato___Early_blight/
│   │   ├── Tomato___Late_blight/
│   │   └── Tomato___healthy/
│   │
│   └── validation/            # Optional validation dataset (or 80/20 auto-split)
│       ├── Apple___Apple_scab/
│       ├── Apple___Black_rot/
│       ├── Apple___healthy/
│       ├── Tomato___Early_blight/
│       ├── Tomato___Late_blight/
│       └── Tomato___healthy/
│
├── uploads/                   # Temporary storage for uploaded test leaves
│
├── templates/
│   ├── index.html             # Main diagnostic landing page
│   ├── result.html            # Dedicated result page for form submissions
│   ├── train.html             # Model training dashboard & metrics
│   └── about.html             # Architecture, stack & methodology documentation
│
└── static/
    ├── css/
    │   └── style.css          # Botanical glassmorphic responsive design system
    ├── js/
    │   └── script.js          # Drag-and-drop, preview & Fetch API logic
    └── images/
        ├── logo.png           # FloraScan AI vector logo
        └── samples/           # Sample leaves for quick testing
            ├── apple_scab.jpg
            ├── corn_rust.jpg
            ├── tomato_early_blight.jpg
            └── tomato_healthy.jpg
```

---

## 🚀 Quick Start Setup Guide

### Step 1 — Create and Activate a Virtual Environment

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

---

### Step 2 — Install Dependencies

```bash
pip install -r requirements.txt
```

---

### Step 3 — Dataset Configuration

The system automatically detects classes from directory subfolders inside `dataset/train/`:

```text
dataset/
└── train/
    ├── Apple___Apple_scab/
    ├── Apple___Black_rot/
    ├── Apple___healthy/
    ├── Tomato___Early_blight/
    ├── Tomato___Late_blight/
    └── Tomato___healthy/
```

> **Note:** A starter dataset is already pre-generated in `dataset/train/` and `dataset/validation/` with 10 representative classes. You can add more folders or replace them with full datasets like **PlantVillage**.

---

### Step 4 — Train the Model

To train or re-train the deep learning model:

```bash
python train.py
```

Optional training arguments:
```bash
python train.py --epochs 10 --batch-size 32 --img-size 224
```

This will:
1. Scan `dataset/train/` for all pathology classes.
2. Initialize MobileNetV2 with ImageNet transfer weights.
3. Apply real-time data augmentations (flips, rotations, zooms).
4. Train and validate the model.
5. Save the trained model to `model/plant_disease_model.keras`.
6. Save class names to `model/class_names.json`.

---

### Step 5 — Start the Flask Web Server

```bash
python app.py
```

---

### Step 6 — Open in Browser

Open your browser and navigate to:
```text
http://127.0.0.1:5000
```

---

## 📡 RESTful API Endpoints

### 1. Leaf Diagnosis: `POST /api/predict`
- **Content-Type:** `multipart/form-data`
- **Body:** `image` (binary file)
- **Response Example:**
```json
{
  "success": true,
  "plant": "Tomato",
  "disease": "Tomato Early Blight",
  "confidence": 98.42,
  "description": "One of the most common tomato diseases worldwide...",
  "symptoms": [
    "Concentric ring target patterns on older leaves near the base",
    "Pronounced yellow chlorotic halos encircling dark lesions"
  ],
  "treatment": [
    "Prune bottom 12 inches of foliage to keep leaves off damp soil.",
    "Apply preventative copper or chlorothalonil fungicides."
  ],
  "top_predictions": [
    {"class_name": "Tomato___Early_blight", "confidence": 98.42},
    {"class_name": "Tomato___Late_blight", "confidence": 1.25}
  ],
  "image_url": "/uploads/leaf_abc123.jpg"
}
```

### 2. System Health: `GET /api/health`
- **Response Example:**
```json
{
  "status": "ok",
  "model_loaded": true,
  "classes_count": 10,
  "uptime": "operational"
}
```

### 3. Background Training: `POST /api/train`
- **JSON Body:** `{"epochs": 5, "batch_size": 16}`
- **Response:** Dispatches training in an asynchronous daemon worker.

### 4. Training Status: `GET /api/train/status`
- **Response:** Returns real-time training progress, metrics, and terminal logs.

---

## 🧪 Consistency and Verification Checklist

| Component | Target File | Verification Status |
| :--- | :--- | :--- |
| **Flask Server** | [app.py](file:///c:/Users/PythonTeam/Desktop/PlantDiseaseProject/app.py) | ✅ Fully operational, tested |
| **Training Pipeline** | [train.py](file:///c:/Users/PythonTeam/Desktop/PlantDiseaseProject/train.py) | ✅ Verified without CLI args |
| **Inference Pipeline** | [predict.py](file:///c:/Users/PythonTeam/Desktop/PlantDiseaseProject/predict.py) | ✅ Verified end-to-end |
| **Disease Knowledge Base** | [disease_info.py](file:///c:/Users/PythonTeam/Desktop/PlantDiseaseProject/disease_info.py) | ✅ 25+ diseases + dynamic fallback |
| **HTML Templates** | `templates/*.html` | ✅ index, result, train, about |
| **Styles & Assets** | `static/css`, `static/js`, `static/images` | ✅ Glassmorphism, animations, logo |

---

## ⚠️ Agricultural Advisory Disclaimer

FloraScan AI predictions are provided for **educational, experimental, and screening purposes only**. Computer vision models can experience misclassifications due to lighting artifacts, camera angle, or unseen pathogen variants. Before purchasing or applying chemical crop treatments, always consult a certified agronomist or regional agricultural extension specialist.
