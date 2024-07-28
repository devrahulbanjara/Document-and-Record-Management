import os
import json
from PIL import Image

# Define paths
val_images_path = r"C:\Users\drenergydrink\Desktop\Document-and-Record-Management\yolooooo\dataset\images\val"
val_annotations_path = r"C:\Users\drenergydrink\Desktop\Document-and-Record-Management\yolooooo\dataset\labels\val"
output_val_json = os.path.join(os.getcwd(), "val_annotations.json")

# Define class names
class_names = [
    'License_Number', 'Name', 'Blood_Group', 'Address', 'DOB',
    'Father_Name', 'Citizenship_Number', 'Phone_Number', 'License_Category', 'License_Type'
]
categories = [{'id': i, 'name': name} for i, name in enumerate(class_names)]

def get_image_info(file_name, img_id):
    with Image.open(file_name) as img:
        width, height = img.size
    return {
        "id": img_id,
        "file_name": os.path.basename(file_name),
        "width": width,
        "height": height
    }

def get_annotation_info(ann_line, img_id, ann_id):
    parts = list(map(float, ann_line.strip().split()))
    category_id = int(parts[0])
    bbox = [
        parts[1] - parts[3] / 2,  # x_min
        parts[2] - parts[4] / 2,  # y_min
        parts[3],                 # width
        parts[4]                  # height
    ]
    return {
        "id": ann_id,
        "image_id": img_id,
        "category_id": category_id,
        "bbox": bbox,
        "area": bbox[2] * bbox[3],
        "iscrowd": 0
    }

def convert_annotations(image_path, annotations_path, output_json):
    images = []
    annotations = []
    ann_id = 1

    for img_id, file_name in enumerate(os.listdir(image_path), 1):
        if file_name.endswith('.jpg'):
            image_info = get_image_info(os.path.join(image_path, file_name), img_id)
            images.append(image_info)

            ann_file = os.path.join(annotations_path, file_name.replace('.jpg', '.txt'))
            if os.path.exists(ann_file):
                with open(ann_file, 'r') as f:
                    for line in f:
                        annotation_info = get_annotation_info(line, img_id, ann_id)
                        annotations.append(annotation_info)
                        ann_id += 1

    coco_format = {
        "images": images,
        "annotations": annotations,
        "categories": categories
    }

    with open(output_json, 'w') as f:
        json.dump(coco_format, f, indent=4)

convert_annotations(val_images_path, val_annotations_path, output_val_json)
