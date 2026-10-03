"""
Utility script to initialize starter dataset folders with representative sample images
and install the application logo to static/images/logo.png.
"""

import os
import shutil
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

PROJECT_ROOT = Path(__file__).resolve().parent
DATASET_DIR = PROJECT_ROOT / "dataset"
TRAIN_DIR = DATASET_DIR / "train"
VAL_DIR = DATASET_DIR / "validation"
STATIC_IMG_DIR = PROJECT_ROOT / "static" / "images"

# Target classes for the starter dataset
CLASSES = [
    "Apple___Apple_scab",
    "Apple___Black_rot",
    "Apple___healthy",
    "Tomato___Early_blight",
    "Tomato___Late_blight",
    "Tomato___healthy",
    "Corn___Common_rust",
    "Potato___Early_blight",
    "Potato___Late_blight",
    "Potato___healthy"
]


def draw_leaf(width=256, height=256, base_color=(45, 120, 50), leaf_type="oval"):
    """Creates a realistic synthetic plant leaf canvas with venation and natural variance."""
    # Background: soft neutral greenhouse / soil / white backdrop
    bg_tone = np.random.randint(235, 250)
    img = Image.new("RGB", (width, height), (bg_tone, bg_tone - 5, bg_tone - 10))
    draw = ImageDraw.Draw(img)

    # Leaf boundary coordinates
    cx, cy = width // 2, height // 2
    r_w = np.random.randint(70, 95)
    r_h = np.random.randint(90, 115)

    # Leaf shape
    leaf_polygon = [
        (cx, cy - r_h),
        (cx + int(r_w * 0.8), cy - int(r_h * 0.4)),
        (cx + r_w, cy + int(r_h * 0.2)),
        (cx + int(r_w * 0.4), cy + int(r_h * 0.85)),
        (cx, cy + r_h),
        (cx - int(r_w * 0.4), cy + int(r_h * 0.85)),
        (cx - r_w, cy + int(r_h * 0.2)),
        (cx - int(r_w * 0.8), cy - int(r_h * 0.4)),
    ]
    draw.polygon(leaf_polygon, fill=base_color)

    # Central midrib stem
    stem_color = (
        min(255, base_color[0] + 30),
        min(255, base_color[1] + 30),
        min(255, base_color[2] + 20)
    )
    draw.line([(cx, cy - r_h + 10), (cx, cy + r_h)], fill=stem_color, width=3)

    # Lateral veins
    for offset_y in range(-r_h + 30, r_h - 20, 25):
        y_pos = cy + offset_y
        span = int(r_w * (1 - abs(offset_y) / (r_h + 10)) * 0.8)
        draw.line([(cx, y_pos), (cx + span, y_pos - 15)], fill=stem_color, width=2)
        draw.line([(cx, y_pos), (cx - span, y_pos - 15)], fill=stem_color, width=2)

    return img, (cx, cy, r_w, r_h)


def add_pathology(img, class_name, geom):
    """Draws class-specific visual symptoms onto the leaf."""
    draw = ImageDraw.Draw(img)
    cx, cy, r_w, r_h = geom

    if "healthy" in class_name:
        # Pristine leaf - maybe slight natural chlorophyll shading
        return img

    if "Apple_scab" in class_name:
        # Olive-green to brownish-black velvety scab spots
        for _ in range(np.random.randint(6, 12)):
            ox = cx + np.random.randint(-int(r_w * 0.6), int(r_w * 0.6))
            oy = cy + np.random.randint(-int(r_h * 0.6), int(r_h * 0.6))
            rad = np.random.randint(6, 14)
            # Scab spot with dark center and olive border
            draw.ellipse([ox - rad, oy - rad, ox + rad, oy + rad], fill=(50, 45, 30))
            draw.ellipse([ox - rad + 2, oy - rad + 2, ox + rad - 2, oy + rad - 2], fill=(25, 20, 15))

    elif "Black_rot" in class_name:
        # Concentric dark lesions with brownish tan centers (frog-eye)
        for _ in range(np.random.randint(5, 10)):
            ox = cx + np.random.randint(-int(r_w * 0.6), int(r_w * 0.6))
            oy = cy + np.random.randint(-int(r_h * 0.6), int(r_h * 0.6))
            rad = np.random.randint(10, 22)
            draw.ellipse([ox - rad - 3, oy - rad - 3, ox + rad + 3, oy + rad + 3], fill=(130, 40, 20))
            draw.ellipse([ox - rad, oy - rad, ox + rad, oy + rad], fill=(30, 20, 20))
            draw.ellipse([ox - rad // 2, oy - rad // 2, ox + rad // 2, oy + rad // 2], fill=(160, 110, 60))

    elif "Early_blight" in class_name:
        # Concentric target bullseye rings with yellow chlorotic halo
        for _ in range(np.random.randint(4, 8)):
            ox = cx + np.random.randint(-int(r_w * 0.6), int(r_w * 0.6))
            oy = cy + np.random.randint(-int(r_h * 0.6), int(r_h * 0.6))
            rad = np.random.randint(14, 28)
            # Yellow chlorotic halo
            draw.ellipse([ox - rad - 6, oy - rad - 6, ox + rad + 6, oy + rad + 6], fill=(190, 180, 40))
            # Brown outer ring
            draw.ellipse([ox - rad, oy - rad, ox + rad, oy + rad], fill=(70, 45, 25))
            # Concentric lighter ring
            draw.ellipse([ox - int(rad * 0.6), oy - int(rad * 0.6), ox + int(rad * 0.6), oy + int(rad * 0.6)], fill=(110, 75, 45))
            # Dark necrotic center
            draw.ellipse([ox - int(rad * 0.3), oy - int(rad * 0.3), ox + int(rad * 0.3), oy + int(rad * 0.3)], fill=(40, 25, 15))

    elif "Late_blight" in class_name:
        # Large irregular water-soaked dark gray/brown necrotic blotches
        for _ in range(np.random.randint(3, 6)):
            ox = cx + np.random.randint(-int(r_w * 0.7), int(r_w * 0.7))
            oy = cy + np.random.randint(-int(r_h * 0.7), int(r_h * 0.7))
            rad_x = np.random.randint(16, 35)
            rad_y = np.random.randint(14, 28)
            draw.ellipse([ox - rad_x, oy - rad_y, ox + rad_x, oy + rad_y], fill=(55, 60, 45))
            draw.ellipse([ox - rad_x + 4, oy - rad_y + 4, ox + rad_x - 4, oy + rad_y - 4], fill=(35, 30, 25))

    elif "Common_rust" in class_name:
        # Bright cinnamon-brown powdery pustules
        for _ in range(np.random.randint(25, 45)):
            ox = cx + np.random.randint(-int(r_w * 0.7), int(r_w * 0.7))
            oy = cy + np.random.randint(-int(r_h * 0.8), int(r_h * 0.8))
            rad = np.random.randint(2, 5)
            draw.ellipse([ox - rad, oy - rad, ox + rad, oy + rad], fill=(185, 80, 20))

    return img


def setup_dataset():
    """Generates training and validation image sets for all target classes."""
    print("Setting up starter dataset folders...")
    for split, count in [("train", 12), ("validation", 4)]:
        split_dir = DATASET_DIR / split
        split_dir.mkdir(parents=True, exist_ok=True)
        
        for cname in CLASSES:
            class_folder = split_dir / cname
            class_folder.mkdir(parents=True, exist_ok=True)
            
            # Determine base color per crop
            if "Apple" in cname:
                base_color = (40, 115, 45)
            elif "Tomato" in cname:
                base_color = (35, 125, 50)
            elif "Corn" in cname:
                base_color = (75, 140, 50)
            elif "Potato" in cname:
                base_color = (45, 110, 40)
            else:
                base_color = (40, 120, 45)

            for i in range(1, count + 1):
                img_path = class_folder / f"leaf_{i:03d}.jpg"
                if not img_path.exists():
                    # Generate sample with slight color variance
                    color_variant = (
                        max(0, min(255, base_color[0] + np.random.randint(-10, 10))),
                        max(0, min(255, base_color[1] + np.random.randint(-10, 10))),
                        max(0, min(255, base_color[2] + np.random.randint(-10, 10))),
                    )
                    leaf_img, geom = draw_leaf(224, 224, base_color=color_variant)
                    leaf_img = add_pathology(leaf_img, cname, geom)
                    leaf_img.save(img_path, quality=90)
    print("Dataset structure and initial samples successfully initialized!")


def setup_logo():
    """Copies or creates static/images/logo.png."""
    STATIC_IMG_DIR.mkdir(parents=True, exist_ok=True)
    target_logo = STATIC_IMG_DIR / "logo.png"

    # Search for the generated logo in brain artifacts
    artifact_logo = Path(r"C:\Users\PythonTeam\.gemini\antigravity-ide\brain\f21e8244-c045-4e88-8709-da42fd33d5f7\plant_logo_1791003806214.jpg")
    
    if artifact_logo.exists():
        img = Image.open(artifact_logo)
        img.save(target_logo, format="PNG")
        print(f"Copied generated logo to {target_logo}")
    else:
        # Fallback create a high-res clean botanical icon
        img = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.ellipse([16, 16, 240, 240], fill=(16, 185, 129, 255))
        draw.text((70, 110), "LEAF AI", fill=(255, 255, 255, 255))
        img.save(target_logo, format="PNG")
        print(f"Created fallback logo at {target_logo}")


def setup_samples():
    """Generates sample test leaf images in static/images/samples for one-click testing in index.html."""
    sample_dir = STATIC_IMG_DIR / "samples"
    sample_dir.mkdir(parents=True, exist_ok=True)
    
    samples_map = {
        "apple_scab.jpg": ("Apple___Apple_scab", (40, 115, 45)),
        "tomato_early_blight.jpg": ("Tomato___Early_blight", (35, 125, 50)),
        "corn_rust.jpg": ("Corn___Common_rust", (75, 140, 50)),
        "tomato_healthy.jpg": ("Tomato___healthy", (35, 125, 50))
    }

    for fname, (cname, color) in samples_map.items():
        sample_path = sample_dir / fname
        if not sample_path.exists():
            leaf_img, geom = draw_leaf(224, 224, base_color=color)
            leaf_img = add_pathology(leaf_img, cname, geom)
            leaf_img.save(sample_path, quality=92)
            print(f"Generated sample image: {sample_path}")


if __name__ == "__main__":
    setup_dataset()
    setup_logo()
    setup_samples()

