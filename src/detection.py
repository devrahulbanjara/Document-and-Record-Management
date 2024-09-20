import easyocr
from paddleocr import PaddleOCR
import streamlit as st
from ultralytics import YOLO
import numpy as np

license_model_path = r"../trained models/License_model.pt"
citizenship_model_path = r"../trained models/Citizenship_model.pt"
passport_model_path = r"../trained models/withoutdocumenttype_Passport_model.pt"

license_model = YOLO(license_model_path)
citizenship_model = YOLO(citizenship_model_path)
passport_model = YOLO(passport_model_path)

class_mappings = {
    "License": {
        0: 'citizenship_number',
        1: 'contact_number',
        2: 'dob',
        3: 'license_number',
        4: 'name'
    },
    "Citizenship": {
        0: 'citizenship_number',
        1: 'district',
        2: 'gender',
        3: 'name',
        4: 'year'
    },
    "Passport": {
        0: 'citizenship_number',
        1: 'dob',
        2: 'name',
        3: 'passport_number',
        4: 'surname',
    }
}

def detector(pred_class, img_bgr):
    if pred_class == "License":
        st.write("Processing License document...")
        results = license_model(img_bgr)
        ocr = PaddleOCR(use_angle_cls=True, lang='en',use_gpu=False)
        
    elif pred_class == "Citizenship":
        st.write("Processing Citizenship document...")
        results = citizenship_model(img_bgr)
        ocr = easyocr.Reader(["ne"],gpu=True)
    elif pred_class == "Passport":
        st.write("Processing Passport document...")
        results = passport_model(img_bgr)
        ocr = PaddleOCR(use_angle_cls=True, lang='en',use_gpu=False)
        
    else:
        st.write('Document type not supported for detailed processing.')
        st.image(img_array, caption="Original Image")
        st.stop()
        
    collected_texts = {label: [] for label in class_mappings[pred_class].values()}
    highest_conf_boxes = {}

    for result in results:
        if result.boxes is not None:
            boxes = result.boxes.xyxy.cpu().numpy()
            class_ids = result.boxes.cls.cpu().numpy()
            confidences = result.boxes.conf.cpu().numpy()

            for i in range(len(class_ids)):
                class_id = int(class_ids[i])
                confidence = confidences[i]
                x1, y1, x2, y2 = map(int, boxes[i].tolist())
                label = class_mappings[pred_class].get(class_id, "Unknown")

                if label not in highest_conf_boxes or confidence > highest_conf_boxes[label][1]:
                    highest_conf_boxes[label] = [(x1, y1, x2, y2), confidence]
    
    return highest_conf_boxes, ocr, collected_texts