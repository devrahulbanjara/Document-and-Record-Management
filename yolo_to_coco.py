import os
import json
import random
import shutil
from PIL import Image

fields = {
    "License_Number": ((114, 101), 160, 25),
    "Name": ((348, 100), 226, 25),
    "Blood_Group": ((93, 129), 70, 25),
    "Address": ((378, 129), 200, 90),
    "DOB": ((355, 217), 226, 25),
    "Father_Name": ((384, 248), 190, 25),
    "Citizenship_Number": ((425, 278), 160, 25),
    "Phone_Number": ((390, 337), 190, 25),
    "License_Category": ((675, 283), 70, 25),
    "License_Type": ((275, 64), 228, 24)
}

image_folder = r"C:\Users\drenergydrink\Desktop\Document-and-Record-Management\License_generator\output_images"
train_folder = r"C:\Users\drenergydrink\Desktop\Document-and-Record-Management\License_generator\train_images"
val_folder = r"C:\Users\drenergydrink\Desktop\Document-and-Record-Management\License_generator\val_images"
output_train_json = "output_train_coco.json"
output_val_json = "output_val_coco.json"

# Create directories if they do not exist
os.makedirs(train_folder, exist_ok=True)
os.makedirs(val_folder, exist_ok=True)

categories = [{"supercategories": field, "id": idx + 1, "name": field} for idx, field in enumerate(fields.keys())]
images = []
annotations = []

image_id = 1
annotation_id = 1

for filename in os.listdir(image_folder):
    if filename.startswith("license_") and filename.endswith(".png"):
        file_path = os.path.join(image_folder, filename)
        with Image.open(file_path) as img:
            width, height = img.size

        images.append({
            "id": image_id,
            "width": width,
            "height": height,
            "file_name": filename
        })

        for category_id, (field, ((x, y), w, h)) in enumerate(fields.items(), start=1):
            annotations.append({
                "id": annotation_id,
                "image_id": image_id,
                "category_id": category_id,
                "segmentation": [],
                "area": w * h,
                "bbox": [x, y, w, h],
                "iscrowd": 0
            })
            annotation_id += 1

        image_id += 1

# Shuffle images and split into train and val sets
random.shuffle(images)
split_index = int(0.8 * len(images))
train_images = images[:split_index]
val_images = images[split_index:]

# Separate annotations based on image_id
train_annotations = [ann for ann in annotations if ann["image_id"] in {img["id"] for img in train_images}]
val_annotations = [ann for ann in annotations if ann["image_id"] in {img["id"] for img in val_images}]

# Copy images to train and val directories
for img in train_images:
    shutil.copy(os.path.join(image_folder, img["file_name"]), train_folder)

for img in val_images:
    shutil.copy(os.path.join(image_folder, img["file_name"]), val_folder)

train_coco_format = {
    "categories": categories,
    "images": train_images,
    "annotations": train_annotations
}

val_coco_format = {
    "categories": categories,
    "images": val_images,
    "annotations": val_annotations
}

with open(os.path.join(train_folder, output_train_json), 'w') as f:
    json.dump(train_coco_format, f, indent=4)

with open(os.path.join(val_folder, output_val_json), 'w') as f:
    json.dump(val_coco_format, f, indent=4)

print(f"COCO format JSONs saved to {os.path.join(train_folder, output_train_json)} and {os.path.join(val_folder, output_val_json)}")
