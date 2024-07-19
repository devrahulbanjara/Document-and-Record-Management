import os
from PIL import Image

# Define the classes
classes = ["License_Number", "Name", "Blood_Group", "Address", "DOB", "Father_Name", "Citizenship_Number", "Phone_Number", "License_Category", "License_Type"]

# Define the top-left positions for each field along with their widths and heights, shifted 5 pixels to the left
fields = {
    "License_Number": ((114, 101), 160, 25),  # 119 - 5
    "Name": ((348, 100), 226, 25),  # 353 - 5
    "Blood_Group": ((93, 129), 70, 25),  # 98 - 5
    "Address": ((378, 129), 200, 90),  # 383 - 5
    "DOB": ((355, 217), 226, 25),  # 360 - 5
    "Father_Name": ((384, 248), 190, 25),  # 389 - 5
    "Citizenship_Number": ((425, 278), 160, 25),  # 430 - 5
    "Phone_Number": ((390, 337), 190, 25),  # 395 - 5
    "License_Category": ((675, 283), 70, 25),  # 680 - 5
    "License_Type": ((275, 64), 228, 24)  # 280 - 5
}

# Load the template image to get the image dimensions
template_path = "template.jpg"
template_image = Image.open(template_path)
image_width, image_height = template_image.size

output_dir = "output_images"
annotation_dir = "annotations"
os.makedirs(annotation_dir, exist_ok=True)

def create_annotation(image_index, fields, image_width, image_height):
    annotations = []
    for i, (field, (top_left, width, height)) in enumerate(fields.items()):
        center_x = (top_left[0] + width / 2) / image_width
        center_y = (top_left[1] + height / 2) / image_height
        width /= image_width
        height /= image_height
        annotations.append(f"{i} {center_x} {center_y} {width} {height}")
    
    annotation_path = os.path.join(annotation_dir, f"license_{image_index}.txt")
    with open(annotation_path, 'w') as f:
        f.write("\n".join(annotations))

# Create annotations for each image
for i in range(100):
    create_annotation(i, fields, image_width, image_height)

print("Finished generating annotations.")
