import os
import json
import shutil
from PIL import Image
from sklearn.model_selection import train_test_split

def yolo_to_coco(yolo_dir, image_dir, output_dir, class_names, split_ratio=0.8):
    images = []
    annotations = []
    categories = []
    annotation_id = 1

    # Create output directories if they don't exist
    os.makedirs(os.path.join(output_dir, 'coco128', 'annotations'), exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'coco128', 'train2017'), exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'coco128', 'val2017'), exist_ok=True)

    # Create categories for each class
    for i, class_name in enumerate(class_names):
        categories.append({
            'id': i + 1,
            'name': class_name,
            'supercategory': 'none',
        })

    # Read images and annotations
    img_files = sorted([f for f in os.listdir(image_dir) if f.endswith('.png')])
    ann_files = sorted([f for f in os.listdir(yolo_dir) if f.endswith('.txt')])
    
    assert len(img_files) == len(ann_files), "Number of images and annotations do not match"

    # Split data into train and val sets
    train_imgs, val_imgs, train_anns, val_anns = train_test_split(img_files, ann_files, train_size=split_ratio, random_state=42)
    
    image_id = 0
    for split, img_files, ann_files in zip(['train', 'val'], [train_imgs, val_imgs], [train_anns, val_anns]):
        for img_file, ann_file in zip(img_files, ann_files):
            image_id += 1
            image_path = os.path.join(image_dir, img_file)
            label_path = os.path.join(yolo_dir, ann_file)
            
            with Image.open(image_path) as img:
                width, height = img.size
            
            images.append({
                'file_name': img_file,
                'height': height,
                'width': width,
                'id': image_id,
                'split': split
            })
            
            with open(label_path) as f:
                for line in f:
                    parts = line.strip().split()
                    category_id = int(parts[0]) + 1
                    x_center, y_center, bbox_width, bbox_height = map(float, parts[1:])
                    
                    x_center *= width
                    y_center *= height
                    bbox_width *= width
                    bbox_height *= height
                    
                    x_min = x_center - (bbox_width / 2)
                    y_min = y_center - (bbox_height / 2)
                    
                    annotations.append({
                        'id': annotation_id,
                        'image_id': image_id,
                        'category_id': category_id,
                        'bbox': [x_min, y_min, bbox_width, bbox_height],
                        'area': bbox_width * bbox_height,
                        'iscrowd': 0,
                    })
                    annotation_id += 1
            
            # Copy image to the appropriate folder
            if split == 'train':
                shutil.copy(image_path, os.path.join(output_dir, 'coco128', 'train2017', img_file))
            else:
                shutil.copy(image_path, os.path.join(output_dir, 'coco128', 'val2017', img_file))
        
        coco_format = {
            'images': [img for img in images if img['split'] == split],
            'annotations': [ann for ann in annotations if ann['image_id'] in {img['id'] for img in images if img['split'] == split}],
            'categories': categories,
        }
        
        output_json = os.path.join(output_dir, 'coco128', 'annotations', f'instances_{split}2017.json')
        with open(output_json, 'w') as f:
            json.dump(coco_format, f, indent=4)

# Define your class names here
class_names = ['License_Number', 'Name', 'Blood_Group', 'Address', 'DOB', 'Father_Name', 'Citizenship_Number', 'Phone_Number', 'License_Category', 'License_Type']

# Convert YOLO to COCO
yolo_to_coco(
    yolo_dir='C:/Users/drenergydrink/Desktop/Document-and-Record-Management/License_generator/annotations',
    image_dir='C:/Users/drenergydrink/Desktop/Document-and-Record-Management/License_generator/output_images',
    output_dir='C:/Users/drenergydrink/Desktop/Document-and-Record-Management/yolooooo/dataset',
    class_names=class_names
)
