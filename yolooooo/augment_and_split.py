import os
import random
import shutil

# Paths
image_dir = r'C:\Users\drenergydrink\Desktop\Document-and-Record-Management\License_generator\output_images'
annotation_dir = r'C:\Users\drenergydrink\Desktop\Document-and-Record-Management\License_generator\annotations'
train_image_dir = r'dataset/images/train'
val_image_dir = r'dataset/images/val'
train_label_dir = r'dataset/labels/train'
val_label_dir = r'dataset/labels/val'

# Ensure the destination directories exist
os.makedirs(train_image_dir, exist_ok=True)
os.makedirs(val_image_dir, exist_ok=True)
os.makedirs(train_label_dir, exist_ok=True)
os.makedirs(val_label_dir, exist_ok=True)

# Check if the image directory exists
if not os.path.exists(image_dir):
    print(f"Image directory {image_dir} does not exist.")
else:
    print(f"Image directory {image_dir} exists.")

# List all files in the image directory
all_files = os.listdir(image_dir)
print(f"Files in image directory: {all_files}")

# Get all image files with .png extension
images = [f for f in all_files if f.endswith('.png')]
print(f"Found {len(images)} images")

# Shuffle and split data
random.shuffle(images)
split_idx = int(0.8 * len(images))
train_images = images[:split_idx]
val_images = images[split_idx:]
print(f"Split {len(train_images)} images for training and {len(val_images)} images for validation")

# Function to move files
def move_files(file_list, src_img_dir, src_label_dir, dst_img_dir, dst_label_dir):
    for file_name in file_list:
        # Move image file
        shutil.copy(os.path.join(src_img_dir, file_name), dst_img_dir)
        # Move corresponding label file
        label_name = file_name.replace('.png', '.txt')
        shutil.copy(os.path.join(src_label_dir, label_name), dst_label_dir)
        print(f"Copied {file_name} and {label_name}")

# Move training files
print("Moving training files...")
move_files(train_images, image_dir, annotation_dir, train_image_dir, train_label_dir)
print("Training files moved")

# Move validation files
print("Moving validation files...")
move_files(val_images, image_dir, annotation_dir, val_image_dir, val_label_dir)
print("Validation files moved")
