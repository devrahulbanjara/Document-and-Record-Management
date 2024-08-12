import os
import random
from PIL import Image, ImageDraw

# Paths to directories
template1_annotations_dir = '/home/rahul/Desktop/Document-and-Record-Management/Citizenship Generator/template1_annotations/'
template2_annotations_dir = '/home/rahul/Desktop/Document-and-Record-Management/Citizenship Generator/template2_annotations/'
template1_images_dir = '/home/rahul/Desktop/Document-and-Record-Management/Citizenship Generator/Template1_Generated_image'
template2_images_dir = '/home/rahul/Desktop/Document-and-Record-Management/Citizenship Generator/Template2_Generated_image'

# Output directories for annotated images
template1_output_dir = '/home/rahul/Desktop/Document-and-Record-Management/Citizenship Generator/template1_annotated/'
template2_output_dir = '/home/rahul/Desktop/Document-and-Record-Management/Citizenship Generator/template2_annotated/'

# Create output directories if they do not exist
os.makedirs(template1_output_dir, exist_ok=True)
os.makedirs(template2_output_dir, exist_ok=True)

# Function to read annotation
def read_annotation(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.readlines()
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return []

# Function to draw annotation on image
def draw_annotations(image, annotations):
    draw = ImageDraw.Draw(image)
    for line in annotations:
        parts = line.strip().split()
        if len(parts) < 5:
            print(f"Skipping malformed line: {line.strip()}")
            continue
        try:
            label, x_center, y_center, width, height = map(float, parts)
            width = width * image.width
            height = height * image.height
            x_center = x_center * image.width
            y_center = y_center * image.height
            x1 = x_center - width / 2
            y1 = y_center - height / 2
            x2 = x_center + width / 2
            y2 = y_center + height / 2
            draw.rectangle([x1, y1, x2, y2], outline='red', width=2)
        except Exception as e:
            print(f"Error processing annotation line: {line.strip()} - {e}")
    return image

# Function to save annotated images
def save_annotated_images(annotations_dir, images_dir, output_dir, num_images=5):
    try:
        annotation_files = [f for f in os.listdir(annotations_dir) if f.endswith('.txt')]
        if not annotation_files:
            print(f"No annotation files found in {annotations_dir}")
            return
        
        random_files = random.sample(annotation_files, min(num_images, len(annotation_files)))
        
        for file_name in random_files:
            annotation_path = os.path.join(annotations_dir, file_name)
            annotations = read_annotation(annotation_path)
            
            image_name = file_name.replace('.txt', '.jpg')
            image_path = os.path.join(images_dir, image_name)
            
            if not os.path.exists(image_path):
                print(f"Image file not found: {image_path}")
                continue
            
            img = Image.open(image_path)
            img_with_annotations = draw_annotations(img.copy(), annotations)
            
            output_image_path = os.path.join(output_dir, image_name)
            img_with_annotations.save(output_image_path)
            print(f'Saved annotated image: {output_image_path}')
    
    except Exception as e:
        print(f"Error in save_annotated_images function: {e}")

# Save 5 annotated images from template1 and template2
save_annotated_images(template1_annotations_dir, template1_images_dir, template1_output_dir, num_images=5)
save_annotated_images(template2_annotations_dir, template2_images_dir, template2_output_dir, num_images=5)
