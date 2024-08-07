import os
import json
import cv2

# Define colors for each category for better visualization
colors = {
    "License_Number": (255, 0, 0),
    "Name": (0, 255, 0),
    "Blood_Group": (0, 0, 255),
    "Address": (255, 255, 0),
    "DOB": (0, 255, 255),
    "Father_Name": (255, 0, 255),
    "Citizenship_Number": (128, 0, 128),
    "Phone_Number": (0, 128, 128),
    "License_Category": (128, 128, 0),
    "License_Type": (0, 0, 128)
}

# Paths to image directory and JSON file
image_folder = r"C:\Users\drenergydrink\Desktop\Document-and-Record-Management\COCO\images"
json_path = r"C:\Users\drenergydrink\Desktop\Document-and-Record-Management\COCO\annotations\annotations_coco.json"

# Create a new folder for visualized annotations
visualized_folder = r"C:\Users\drenergydrink\Desktop\Document-and-Record-Management\COCO\visualized_images"
license_visualized_folder = os.path.join(visualized_folder, "license_visualized")

# Ensure the directory exists
os.makedirs(license_visualized_folder, exist_ok=True)

# Function to draw bounding boxes on images
def draw_bounding_boxes(image_folder, json_path, output_folder):
    with open(json_path) as f:
        data = json.load(f)
    
    for img in data["images"]:
        image_path = os.path.join(image_folder, img["file_name"])
        image = cv2.imread(image_path)
        if image is None:
            continue
        
        annotations = [ann for ann in data["annotations"] if ann["image_id"] == img["id"]]
        for ann in annotations:
            category_id = ann["category_id"]
            category_name = data["categories"][category_id - 1]["name"]
            bbox = ann["bbox"]
            color = colors.get(category_name, (0, 0, 0))  # Default to black if color not found
            
            # Draw rectangle and category name on the image
            x, y, w, h = map(int, bbox)
            cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
            cv2.putText(image, category_name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
        
        # Save the image with bounding boxes
        output_image_path = os.path.join(output_folder, img["file_name"])
        cv2.imwrite(output_image_path, image)

# Visualize the images
draw_bounding_boxes(image_folder, json_path, license_visualized_folder)

print("Bounding boxes drawn and images saved.")
