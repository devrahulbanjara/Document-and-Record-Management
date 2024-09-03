import os
from PIL import Image, ImageDraw
import pandas as pd

# Define the annotation colors for different classes
annotation_colors = {
    0: 'red',        # license_number
    1: 'green',      # document_type
    2: 'blue',       # name
    3: 'purple',     # address
    4: 'orange',     # dob
    5: 'pink',       # father_name
    6: 'cyan',       # citizenship_number
    7: 'yellow',     # contact_number
    8: 'magenta',    # license_category
    9: 'lime',       # blood_group
}

# Directory containing images
image_dir = "/mnt/c/Users/drenergydrink/Desktop/Document-and-Record-Management/License Generator/output_images"
# Directory containing YOLO annotations
annotations_dir = "/mnt/c/Users/drenergydrink/Desktop/Document-and-Record-Management/License Generator/annotations"
# Directory to save annotated images
output_dir = "/mnt/c/Users/drenergydrink/Desktop/Document-and-Record-Management/License Generator/annotated_images"
os.makedirs(output_dir, exist_ok=True)

# Function to convert YOLO format to pixel coordinates
def yolo_to_pixels(x_center, y_center, width, height, img_width, img_height):
    x1 = int((x_center - width / 2) * img_width)
    y1 = int((y_center - height / 2) * img_height)
    x2 = int((x_center + width / 2) * img_width)
    y2 = int((y_center + height / 2) * img_height)
    
    # Ensure coordinates are in correct order
    x1, x2 = min(x1, x2), max(x1, x2)
    y1, y2 = min(y1, y2), max(y1, y2)
    
    # Ensure coordinates are within image boundaries
    x1, y1 = max(0, x1), max(0, y1)
    x2, y2 = min(img_width, x2), min(img_height, y2)
    
    return x1, y1, x2, y2

# Visualize YOLO annotations
for i in range(400):  # Assuming 400 images
    img_path = os.path.join(image_dir, f"license_{i}.png")
    annotation_path = os.path.join(annotations_dir, f"license_{i}.txt")
    
    if os.path.exists(img_path) and os.path.exists(annotation_path):
        img = Image.open(img_path)
        draw = ImageDraw.Draw(img)
        img_width, img_height = img.size
        
        with open(annotation_path, 'r') as f:
            for line in f:
                parts = line.strip().split()
                class_id = int(parts[0])
                x_center, y_center, width, height = map(float, parts[1:])
                color = annotation_colors.get(class_id, 'white')
                
                # Convert YOLO format to pixel coordinates
                x1, y1, x2, y2 = yolo_to_pixels(x_center, y_center, width, height, img_width, img_height)
                
                # Draw the bounding box
                if x1 < x2 and y1 < y2:  # Ensure valid bounding box dimensions
                    draw.rectangle([x1, y1, x2, y2], outline=color, width=2)
        
        # Save the annotated image
        output_path = os.path.join(output_dir, f"annotated_license_{i}.png")
        img.save(output_path)

print("Finished visualizing annotations.")
