import os
from PIL import Image, ImageDraw

# Define the classes (same as the annotation script)
classes = ["License_Number", "Name", "Blood_Group", "Address", "DOB", "Father_Name", "Citizenship_Number", "Phone_Number", "License_Category", "License_Type"]

# Directories
output_dir = "output_images"
annotation_dir = "annotations"
visualization_dir = "visualized_images"
os.makedirs(visualization_dir, exist_ok=True)

def draw_annotations(image_path, annotation_path, output_path):
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    image_width, image_height = image.size
    
    with open(annotation_path, 'r') as f:
        for line in f:
            parts = line.strip().split()
            class_id = int(parts[0])
            center_x = float(parts[1]) * image_width
            center_y = float(parts[2]) * image_height
            width = float(parts[3]) * image_width
            height = float(parts[4]) * image_height
            
            top_left_x = center_x - width / 2
            top_left_y = center_y - height / 2
            bottom_right_x = center_x + width / 2
            bottom_right_y = center_y + height / 2
            
            draw.rectangle([top_left_x, top_left_y, bottom_right_x, bottom_right_y], outline="red", width=2)
            draw.text((top_left_x, top_left_y), classes[class_id], fill="red")
    
    image.save(output_path)

# Visualize annotations for each image
for i in range(100):
    image_path = os.path.join(output_dir, f"license_{i}.png")
    annotation_path = os.path.join(annotation_dir, f"license_{i}.txt")
    output_path = os.path.join(visualization_dir, f"visualized_license_{i}.png")
    draw_annotations(image_path, annotation_path, output_path)

print("Finished visualizing annotations.")
