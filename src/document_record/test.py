import cv2
from ultralytics import YOLO
import easyocr
import os
import numpy as np

image_path = '/mnt/c/Users/Rahul/Desktop/Document-and-Record-Management/notebooks/YOLOv8/Biswa-_jpg.rf.b79bbd00d55ce91b0d9ce13f9f1d6686.jpg'
model_path = "/mnt/c/Users/Rahul/Desktop/trained models/Citizenship_model.pt"

model = YOLO(model_path)
results = model(image_path)
image = cv2.imread(image_path)
ocr = easyocr.Reader(['ne', 'en'])

class_map = {
    0: 'citizenship_number',
    1: 'day',
    2: 'district',
    3: 'document_type',
    4: 'father_name',
    5: 'gender',
    6: 'month',
    7: 'municipality',
    8: 'name',
    9: 'ward',
    10: 'year'
}

def get_color(class_id):
    np.random.seed(class_id)
    return tuple(np.random.randint(0, 255, 3).tolist())

base_name = os.path.splitext(os.path.basename(image_path))[0]
output_dir = 'OCR_Outputs'
os.makedirs(output_dir, exist_ok=True)
output_file_path = os.path.join(output_dir, f'{base_name}_results.txt')

collected_texts = {label: [] for label in class_map.values()}

for result in results:
    boxes = result.boxes.xyxy
    class_ids = result.boxes.cls

    for box, class_id in zip(boxes, class_ids):
        x1, y1, x2, y2 = map(int, box.tolist())
        cropped_img = image[y1:y2, x1:x2]

        ocr_result = ocr.readtext(cropped_img)
        for detection in ocr_result:
            text = detection[1]
            label = class_map.get(int(class_id), 'Unknown')
            collected_texts[label].append(text)
            
        color = get_color(int(class_id))
        cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
        cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

with open(output_file_path, 'w') as file:
    for label, texts in collected_texts.items():
        combined_text = ' '.join(texts)
        if combined_text:
            file.write(f"Class: {label}, Text: {combined_text}\n")

annotated_image_path = os.path.join(output_dir, f'{base_name}_annotated.jpg')
cv2.imwrite(annotated_image_path, image)
