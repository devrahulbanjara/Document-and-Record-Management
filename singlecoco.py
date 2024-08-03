import json
import os

# Define the path to the images and annotations
image_dir = r"C:\Users\drenergydrink\Desktop\Document-and-Record-Management\License_generator\output_images"
output_json = "annotations_coco.json"

# Define the categories
categories = [
    {"supercategory": "License_Number", "id": 1, "name": "License_Number"},
    {"supercategory": "Name", "id": 2, "name": "Name"},
    {"supercategory": "Blood_Group", "id": 3, "name": "Blood_Group"},
    {"supercategory": "Address", "id": 4, "name": "Address"},
    {"supercategory": "DOB", "id": 5, "name": "DOB"},
    {"supercategory": "Father_Name", "id": 6, "name": "Father_Name"},
    {"supercategory": "Citizenship_Number", "id": 7, "name": "Citizenship_Number"},
    {"supercategory": "Phone_Number", "id": 8, "name": "Phone_Number"},
    {"supercategory": "License_Category", "id": 9, "name": "License_Category"},
    {"supercategory": "License_Type", "id": 10, "name": "License_Type"},
]

# Initialize the lists
images = []
annotations = []

# Iterate through the images
for idx, filename in enumerate(os.listdir(image_dir)):
    if filename.endswith(".png"):
        image_id = idx + 1
        file_path = os.path.join(image_dir, filename)
        images.append({
            "id": image_id,
            "width": 777,
            "height": 477,
            "file_name": filename
        })

        # Define the bounding boxes for each category
        bboxes = {
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

        for category_id, (name, (top_left, width, height)) in enumerate(bboxes.items(), 1):
            x, y = top_left
            annotations.append({
                "id": len(annotations) + 1,
                "image_id": image_id,
                "category_id": category_id,
                "segmentation": [],
                "area": width * height,
                "bbox": [x, y, width, height],
                "iscrowd": 0
            })

# Combine everything into the final dictionary
coco_format = {
    "categories": categories,
    "images": images,
    "annotations": annotations
}

# Write to the JSON file
with open(output_json, 'w') as f:
    json.dump(coco_format, f, indent=4)

print(f"COCO format annotations saved to {output_json}")
