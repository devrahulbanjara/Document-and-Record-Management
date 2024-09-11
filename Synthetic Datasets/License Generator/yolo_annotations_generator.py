import os
from PIL import Image

# Define the annotation coordinates (top-left and bottom-right)
annotations = {
    "license_number": ((58, 149), (375, 186)),
    "name": ((390, 188), (804, 224)),
    "dob": ((390, 354), (645, 394)),
    "citizenship_number": ((387, 444), (789, 484)),
    "contact_number": ((388, 532), (683, 569)),
}

# Directory containing images
image_dir = "/mnt/c/Users/Rahul/Desktop/Document-and-Record-Management/synthetic Datasets/License Generator/output_images"

# Directory to save YOLO annotations
annotations_dir = "/mnt/c/Users/Rahul/Desktop/Document-and-Record-Management/synthetic Datasets/License Generator/new"
os.makedirs(annotations_dir, exist_ok=True)

# Function to convert coordinates to YOLO format
def convert_to_yolo(x1, y1, x2, y2, img_width, img_height):
    x_center = (x1 + x2) / 2
    y_center = (y1 + y2) / 2
    width = x2 - x1
    height = y2 - y1
    x_center_normalized = x_center / img_width
    y_center_normalized = y_center / img_height
    width_normalized = width / img_width
    height_normalized = height / img_height
    return x_center_normalized, y_center_normalized, width_normalized, height_normalized

# Generate YOLO annotations
for i in range(400):  # Assuming 400 images
    img_path = os.path.join(image_dir, f"license_{i}.png")
    if os.path.exists(img_path):
        img = Image.open(img_path)
        img_width, img_height = img.size
        
        # Open corresponding YOLO annotation file
        annotation_file = os.path.join(annotations_dir, f"license_{i}.txt")
        with open(annotation_file, 'w') as f:
            for class_id, (label, ((x1, y1), (x2, y2))) in enumerate(annotations.items()):
                x_center, y_center, width, height = convert_to_yolo(x1, y1, x2, y2, img_width, img_height)
                # Writing to YOLO format: class_id x_center y_center width height
                f.write(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")

print("Finished generating YOLO annotations.")
