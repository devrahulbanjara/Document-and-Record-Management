import streamlit as st
from PIL import Image
import numpy as np
import easyocr
import tensorflow as tf
from tensorflow.keras.preprocessing import image as keras_image
from keras.applications.resnet50 import preprocess_input
from ultralytics import YOLO
import cv2

database_path = "database.json"
Classification_model_path = "/mnt/c/Users/Rahul/Desktop/trained models/Classification_model.h5"
classification_model = tf.keras.models.load_model(Classification_model_path)

st.write("Document and Record Management")
st.write("Please insert a document image (Citizenship, Driving License or Passport)")

uploaded_image = st.file_uploader("Choose an image", type=['png', 'jpg'])

license_model_path = r"/mnt/c/Users/Rahul/Desktop/trained models/License_model.pt"
citizenship_model_path = r"/mnt/c/Users/Rahul/Desktop/trained models/Citizenship_model.pt"
passport_model_path = r"/mnt/c/Users/Rahul/Desktop/trained models/withdocumenttypw_Passport_model.pt"

license_model = YOLO(license_model_path)
citizenship_model = YOLO(citizenship_model_path)
passport_model = YOLO(passport_model_path)

class_mapping_for_classification = {
    0: 'Citizenship',
    1: 'License',
    2: 'Passport',
    3: 'Other documents'
}

license_class_mapping = {
    0: 'citizenship_number',
    1: 'contact_number',
    2: 'dob',
    3: 'license_number',
    4: 'name'
}

if uploaded_image:
    st.write("Image uploaded")
    img = Image.open(uploaded_image)
    img = img.convert('RGB')
    img_array = np.array(img)

    img_resized = cv2.resize(img_array, (500, 500))
    img_expanded = np.expand_dims(img_resized, axis=0)
    img_preprocessed = preprocess_input(img_expanded)

    predictions = classification_model.predict(img_preprocessed)
    predicted_class_index = np.argmax(predictions, axis=1)[0]
    confidence = np.max(predictions)

    predicted_class_label = class_mapping_for_classification[predicted_class_index]
    st.write('Predicted class: ' + predicted_class_label)
    st.write('Confidence: ' + str(confidence))

    img_gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    img_bgr = cv2.cvtColor(img_gray, cv2.COLOR_GRAY2BGR)

    if predicted_class_label == "License":
        ocr = easyocr.Reader(["en"])
        st.write("Processing License document...")

        results = license_model(img_bgr)
        
        collected_texts = {label: [] for label in license_class_mapping.values()}
        highest_conf_boxes = {}

        for result in results:
            boxes = result.boxes.xyxy
            class_ids = result.boxes.cls
            confidences = result.boxes.conf

            for i in range(len(class_ids)):
                class_id = int(class_ids[i])
                confidence = confidences[i]
                x1, y1, x2, y2 = map(int, boxes[i].tolist())
                label = license_class_mapping.get(class_id, "Unknown")

                # Update highest confidence box for each class
                if label not in highest_conf_boxes or confidence > highest_conf_boxes[label][1]:
                    highest_conf_boxes[label] = [(x1, y1, x2, y2), confidence]

        # Draw bounding boxes and process OCR for the highest confidence boxes
        for label, (box, confidence) in highest_conf_boxes.items():
            x1, y1, x2, y2 = box
            cropped_img = img_bgr[y1:y2, x1:x2]
            
            ocr_result = ocr.readtext(cropped_img)
            
            for detection in ocr_result:
                text = detection[1]
                collected_texts[label].append(text)

            color = (255, 255, 255)
            thickness = 4
            font_scale = 1.5
            font_thickness = 3

            cv2.rectangle(img_bgr, (x1, y1), (x2, y2), color, thickness)
            cv2.putText(img_bgr, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, font_thickness)
        
        st.image(cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB), caption="Processed Image")

    elif predicted_class_label == "Citizenship":
        ocr = easyocr.Reader(["np","en"])
        st.write("Processing Citizenship document...")
        results = citizenship_model(img_gray)
        
        collected_texts = {label: [] for label in license_class_mapping.values()}
        highest_conf_boxes = {}
        
        for result in results:
            boxes = result.boxes.xyxy
            class_ids = result.boxes.cls
            confidences = result.boxes.conf

            for i in range(len(class_ids)):
                class_id = int(class_ids[i])
                confidence = confidences[i]
                x1, y1, x2, y2 = map(int, boxes[i].tolist())
                label = license_class_mapping.get(class_id, "Unknown")

                # Update highest confidence box for each class
                if label not in highest_conf_boxes or confidence > highest_conf_boxes[label][1]:
                    highest_conf_boxes[label] = [(x1, y1, x2, y2), confidence]

        # Draw bounding boxes and process OCR for the highest confidence boxes
        for label, (box, confidence) in highest_conf_boxes.items():
            x1, y1, x2, y2 = box
            cropped_img = img_bgr[y1:y2, x1:x2]
            
            ocr_result = ocr.readtext(cropped_img)
            
            for detection in ocr_result:
                text = detection[1]
                collected_texts[label].append(text)

            color = (255, 255, 255)
            thickness = 4
            font_scale = 1.5
            font_thickness = 3

            cv2.rectangle(img_bgr, (x1, y1), (x2, y2), color, thickness)
            cv2.putText(img_bgr, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, font_thickness)
        
        st.image(cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB), caption="Processed Image")
            
    elif predicted_class_label == "Passport":
        ocr = easyocr.Reader("en")
        st.write("Processing License document...")
        results = citizenship_model(img_gray)
        
        collected_texts = {label: [] for label in license_class_mapping.values()}
        highest_conf_boxes = {}
        
        for result in results:
            boxes = result.boxes.xyxy
            class_ids = result.boxes.cls
            confidences = result.boxes.conf

            for i in range(len(class_ids)):
                class_id = int(class_ids[i])
                confidence = confidences[i]
                x1, y1, x2, y2 = map(int, boxes[i].tolist())
                label = license_class_mapping.get(class_id, "Unknown")

                # Update highest confidence box for each class
                if label not in highest_conf_boxes or confidence > highest_conf_boxes[label][1]:
                    highest_conf_boxes[label] = [(x1, y1, x2, y2), confidence]

        # Draw bounding boxes and process OCR for the highest confidence boxes
        for label, (box, confidence) in highest_conf_boxes.items():
            x1, y1, x2, y2 = box
            cropped_img = img_bgr[y1:y2, x1:x2]
            
            ocr_result = ocr.readtext(cropped_img)
            
            for detection in ocr_result:
                text = detection[1]
                collected_texts[label].append(text)

            color = (255, 255, 255)
            thickness = 4
            font_scale = 1.5
            font_thickness = 3

            cv2.rectangle(img_bgr, (x1, y1), (x2, y2), color, thickness)
            cv2.putText(img_bgr, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, font_thickness)
        
        st.image(cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB), caption="Processed Image")
