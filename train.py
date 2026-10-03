"""
train.py - Standalone model training pipeline for Plant Disease Classification.
Employs Transfer Learning using MobileNetV2 pretrained on ImageNet.
Automatically handles dataset discovery, preprocessing, augmentation, training,
evaluation, and saving model weights & class labels.
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np

# Suppress verbose TensorFlow C++ logs
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"


def parse_arguments() -> argparse.Namespace:
    """Parses command-line arguments for training configuration."""
    parser = argparse.ArgumentParser(
        description="Train a CNN for Plant Disease Classification using Transfer Learning (MobileNetV2)."
    )
    parser.add_argument(
        "--data-dir",
        type=str,
        default="dataset",
        help="Root directory containing 'train' (and optionally 'validation') folders."
    )
    parser.add_argument(
        "--model-dir",
        type=str,
        default="model",
        help="Directory to save the trained model (.keras) and class_names.json."
    )
    parser.add_argument(
        "--epochs",
        type=int,
        default=5,
        help="Number of training epochs (default: 5)."
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=16,
        help="Batch size for data loaders (default: 16)."
    )
    parser.add_argument(
        "--img-size",
        type=int,
        default=224,
        help="Target square image resolution in pixels (default: 224)."
    )
    parser.add_argument(
        "--learning-rate",
        type=float,
        default=1e-3,
        help="Initial learning rate for Adam optimizer (default: 0.001)."
    )
    return parser.parse_args()


def discover_classes_and_validate(train_dir: Path) -> List[str]:
    """
    Scans the train directory to identify valid class subdirectories.
    Returns sorted list of class names.
    Raises ValueError if train directory is missing or contains no image classes.
    """
    if not train_dir.exists() or not train_dir.is_dir():
        raise FileNotFoundError(
            f"Training directory '{train_dir}' was not found. "
            f"Please ensure '{train_dir}' exists with subfolders for each disease class."
        )

    valid_extensions = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}
    class_folders = []

    for item in sorted(train_dir.iterdir()):
        if item.is_dir() and not item.name.startswith("."):
            # Check if this folder contains at least one supported image
            images = [f for f in item.iterdir() if f.is_file() and f.suffix.lower() in valid_extensions]
            if len(images) > 0:
                class_folders.append(item.name)

    if not class_folders:
        raise ValueError(
            f"No image classes found in '{train_dir}'. "
            "Please create subdirectories named after each class (e.g. 'Tomato___Early_blight') "
            "and place corresponding leaf images inside."
        )

    return sorted(class_folders)


def build_transfer_learning_model(
    num_classes: int,
    img_size: int = 224,
    learning_rate: float = 1e-3
):
    """
    Constructs an image classification model using MobileNetV2 as a frozen feature extractor,
    paired with custom classification head and data augmentation layers.
    """
    import tensorflow as tf
    from tensorflow.keras import layers, models
    from tensorflow.keras.applications import MobileNetV2
    from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

    # Input layer
    inputs = layers.Input(shape=(img_size, img_size, 3), name="input_image")

    # Data Augmentation pipeline (active only during training)
    x = layers.RandomFlip("horizontal_and_vertical", name="aug_flip")(inputs)
    x = layers.RandomRotation(0.15, name="aug_rotation")(x)
    x = layers.RandomZoom(0.15, name="aug_zoom")(x)
    x = layers.RandomContrast(0.1, name="aug_contrast")(x)

    # Preprocessing: scales [0, 255] to [-1, 1] (native standard MobileNetV2 normalization)
    x = layers.Rescaling(scale=1.0 / 127.5, offset=-1.0, name="mobilenetv2_rescaling")(x)

    # Pretrained MobileNetV2 feature extractor
    base_model = MobileNetV2(
        input_shape=(img_size, img_size, 3),
        include_top=False,
        weights="imagenet"
    )
    base_model.trainable = False  # Freeze base weights for stable transfer learning

    x = base_model(x, training=False)

    # Classification Head
    x = layers.GlobalAveragePooling2D(name="global_avg_pool")(x)
    x = layers.BatchNormalization(name="batch_norm")(x)
    x = layers.Dropout(0.3, name="head_dropout_1")(x)
    x = layers.Dense(128, activation="relu", name="dense_features")(x)
    x = layers.Dropout(0.2, name="head_dropout_2")(x)
    outputs = layers.Dense(num_classes, activation="softmax", name="predictions")(x)

    model = models.Model(inputs=inputs, outputs=outputs, name="PlantDiseaseClassifier")

    # Compile model with standard cross-entropy and accuracy metrics
    optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)
    model.compile(
        optimizer=optimizer,
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )

    return model


def train_pipeline(
    data_dir_path: str = "dataset",
    model_dir_path: str = "model",
    epochs: int = 5,
    batch_size: int = 16,
    img_size: int = 224,
    learning_rate: float = 1e-3,
    progress_callback=None
) -> Dict[str, any]:
    """
    Executes the full training pipeline:
    1. Validates dataset
    2. Builds training and validation tf.data.Dataset
    3. Builds MobileNetV2 model
    4. Trains the model
    5. Saves .keras model and class_names.json
    6. Returns metrics dictionary
    """
    import tensorflow as tf

    start_time = time.time()
    data_dir = Path(data_dir_path).resolve()
    model_dir = Path(model_dir_path).resolve()
    train_dir = data_dir / "train"
    val_dir = data_dir / "validation"

    print("=" * 65)
    print("      PLANT DISEASE CLASSIFICATION - MODEL TRAINING PIPELINE")
    print("=" * 65)
    print(f"Data root directory:   {data_dir}")
    print(f"Model output directory: {model_dir}")
    print(f"Target image size:     {img_size}x{img_size} px")
    print(f"Batch size:            {batch_size}")
    print(f"Target epochs:         {epochs}")
    print(f"Learning rate:         {learning_rate}")
    print("-" * 65)

    # 1. Discover classes and ensure valid data exists
    class_names = discover_classes_and_validate(train_dir)
    num_classes = len(class_names)
    print(f"Found {num_classes} plant pathology classes:")
    for idx, cname in enumerate(class_names, 1):
        print(f"  [{idx:02d}] {cname}")
    print("-" * 65)

    # 2. Check validation dataset setup
    has_explicit_val = False
    if val_dir.exists() and val_dir.is_dir():
        try:
            val_classes = discover_classes_and_validate(val_dir)
            if set(val_classes) == set(class_names):
                has_explicit_val = True
                print("Explicit validation directory detected with matching class labels.")
        except Exception:
            has_explicit_val = False

    # 3. Load datasets using tf.keras.utils.image_dataset_from_directory
    if has_explicit_val:
        print("Loading training dataset from 'train' folder...")
        train_ds = tf.keras.utils.image_dataset_from_directory(
            str(train_dir),
            labels="inferred",
            label_mode="int",
            class_names=class_names,
            image_size=(img_size, img_size),
            batch_size=batch_size,
            shuffle=True,
            seed=42
        )
        print("Loading validation dataset from 'validation' folder...")
        val_ds = tf.keras.utils.image_dataset_from_directory(
            str(val_dir),
            labels="inferred",
            label_mode="int",
            class_names=class_names,
            image_size=(img_size, img_size),
            batch_size=batch_size,
            shuffle=False
        )
    else:
        print("Creating 80/20 train/validation split from 'train' folder...")
        train_ds, val_ds = tf.keras.utils.image_dataset_from_directory(
            str(train_dir),
            labels="inferred",
            label_mode="int",
            class_names=class_names,
            image_size=(img_size, img_size),
            batch_size=batch_size,
            validation_split=0.2,
            subset="both",
            shuffle=True,
            seed=42
        )

    # Optimize data pipeline caching & prefetching
    AUTOTUNE = tf.data.AUTOTUNE
    train_ds = train_ds.prefetch(buffer_size=AUTOTUNE)
    val_ds = val_ds.prefetch(buffer_size=AUTOTUNE)

    # 4. Build Model
    print("Building MobileNetV2 Transfer Learning Architecture...")
    model = build_transfer_learning_model(
        num_classes=num_classes,
        img_size=img_size,
        learning_rate=learning_rate
    )
    model.summary(print_fn=lambda s: print(f"  {s}"))
    print("-" * 65)

    # Custom training callback for UI updates if provided
    callbacks = []
    if progress_callback:
        class UICallback(tf.keras.callbacks.Callback):
            def on_epoch_end(self, epoch, logs=None):
                progress_callback(epoch + 1, epochs, logs)
        callbacks.append(UICallback())

    # 5. Train Model
    print(f"Beginning training for {epochs} epoch(s)...")
    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=epochs,
        callbacks=callbacks,
        verbose=1
    )

    # 6. Evaluate final metrics
    print("-" * 65)
    print("Evaluating model on validation dataset...")
    val_loss, val_acc = model.evaluate(val_ds, verbose=0)
    train_loss = float(history.history["loss"][-1])
    train_acc = float(history.history["accuracy"][-1])

    # 7. Save Model and Class Names
    model_dir.mkdir(parents=True, exist_ok=True)
    model_save_path = model_dir / "plant_disease_model.keras"
    class_names_path = model_dir / "class_names.json"

    print(f"Saving model to '{model_save_path}'...")
    model.save(str(model_save_path))

    print(f"Saving class names to '{class_names_path}'...")
    with open(class_names_path, "w", encoding="utf-8") as f:
        json.dump(class_names, f, indent=2)

    total_time = round(time.time() - start_time, 2)
    print("=" * 65)
    print("                 TRAINING RUN COMPLETED")
    print("=" * 65)
    print(f"Total training time:   {total_time}s")
    print(f"Classes trained:       {num_classes}")
    print(f"Final Training Loss:   {train_loss:.4f}")
    print(f"Final Training Acc:    {train_acc * 100:.2f}%")
    print(f"Validation Loss:       {val_loss:.4f}")
    print(f"Validation Acc:        {val_acc * 100:.2f}%")
    print(f"Model saved:           {model_save_path}")
    print(f"Class names saved:     {class_names_path}")
    print("=" * 65)

    return {
        "success": True,
        "classes": class_names,
        "num_classes": num_classes,
        "train_loss": round(train_loss, 4),
        "train_accuracy": round(train_acc * 100, 2),
        "val_loss": round(float(val_loss), 4),
        "val_accuracy": round(float(val_acc) * 100, 2),
        "time_seconds": total_time,
        "model_path": str(model_save_path),
        "class_names_path": str(class_names_path)
    }


def main():
    """Main CLI entrypoint."""
    args = parse_arguments()
    try:
        train_pipeline(
            data_dir_path=args.data_dir,
            model_dir_path=args.model_dir,
            epochs=args.epochs,
            batch_size=args.batch_size,
            img_size=args.img_size,
            learning_rate=args.learning_rate
        )
    except Exception as e:
        print(f"\n[TRAINING ERROR] {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
