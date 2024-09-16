import streamlit as st
from PIL import Image, ImageOps
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image as keras_image
from keras.applications.resnet50 import preprocess_input
from ultralytics import YOLO
import cv2
import easyocr
import io

database_path = "database.json"
Classification_model_path = "/mnt/c/Users/Rahul/Desktop/trained models/Classification_model.h5"
license_model_path = r"/mnt/c/Users/Rahul/Desktop/trained models/License_model.pt"
citizenship_model_path = r"/mnt/c/Users/Rahul/Desktop/trained models/Citizenship_model.pt"
passport_model_path = r"/mnt/c/Users/Rahul/Desktop/trained models/withoutdocumenttype_Passport_model.pt"

classification_model = tf.keras.models.load_model(Classification_model_path)
license_model = YOLO(license_model_path)
citizenship_model = YOLO(citizenship_model_path)
passport_model = YOLO(passport_model_path)

class_mapping_for_classification = {
    0: 'Citizenship',
    1: 'License',
    2: 'Passport',
    3: 'Other documents'
}

class_mappings={
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
    "Passport":{
    0: 'citizenship_number',
    1: 'dob',
    2: 'name',
    3: 'passport_number',
    4: 'surname',
    }
    }

def correct_image_orientation(uploaded_file):
    """Corrects image orientation based on EXIF metadata."""
    image = Image.open(uploaded_file)
    image = ImageOps.exif_transpose(image)
    return image

def get_color(class_id):
    np.random.seed(class_id)
    return tuple(np.random.randint(0, 255, 3).tolist())

st.write("Document and Record Management")
st.write("Please insert a document image (Citizenship, Driving License, or Passport)")

uploaded_image = st.file_uploader("Choose an image", type=['png', 'jpg'])

if uploaded_image:
    st.write("Image uploaded")
    
    img = correct_image_orientation(uploaded_image)
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

    ocr = easyocr.Reader(["en"])
    if predicted_class_label == "License":
        st.write("Processing License document...")
        results = license_model(img_bgr)
        
    elif predicted_class_label == "Citizenship":
        st.write("Processing Citizenship document...")
        ocr = easyocr.Reader(["ne","en"])
        results = citizenship_model(img_bgr)
        
    elif predicted_class_label == "Passport":
        st.write("Processing Passport document...")
        results = passport_model(img_bgr)
        
    else:
        st.write('Document type not supported for detailed processing.')
        st.image(img_array, caption="Original Image")
        st.stop()
    
    collected_texts = {label: [] for label in class_mappings[predicted_class_label].values()}
    highest_conf_boxes = {}

    for result in results:
        boxes = result.boxes.xyxy
        class_ids = result.boxes.cls
        confidences = result.boxes.conf

        for i in range(len(class_ids)):
            class_id = int(class_ids[i])
            confidence = confidences[i]
            x1, y1, x2, y2 = map(int, boxes[i].tolist())
            label = class_mappings[predicted_class_label].get(class_id, "Unknown")
            if label not in highest_conf_boxes or confidence > highest_conf_boxes[label][1]:
                highest_conf_boxes[label] = [(x1, y1, x2, y2), confidence]

    for label, (box, confidence) in highest_conf_boxes.items():
        x1, y1, x2, y2 = box
        cropped_img = img_bgr[y1:y2, x1:x2]
        
        ocr_result = ocr.readtext(cropped_img)
        
        for detection in ocr_result:
            text = detection[1]
            collected_texts[label].append(text)

        color = get_color(int(class_id))
        font_scale = 1.5
        font_thickness = 3

        cv2.rectangle(img_bgr, (x1, y1), (x2, y2), color, 2)
        cv2.putText(img_bgr, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, font_thickness)
    
    st.image(cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB), caption="Processed Image")
    st.write("Extracted Texts:")
    
    with open("database.json","w") as db:
        for label, texts in collected_texts.items():
            st.write(f"{label}: {'; '.join(texts)}")
