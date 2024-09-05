import os
import cv2

def convert_to_grayscale(folder_path):
    for image_name in os.listdir(folder_path):
        if image_name.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(folder_path, image_name)
            image = cv2.imread(image_path)
            grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            cv2.imwrite(image_path, grayscale_image)

folder1 = "/mnt/c/Users/Rahul/Desktop/datasets/License with annotations/train/images"
folder2 = "/mnt/c/Users/Rahul/Desktop/datasets/License with annotations/valid/images"

convert_to_grayscale(folder1)
convert_to_grayscale(folder2)
