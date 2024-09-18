import streamlit as st
from PIL import Image, ImageOps
import numpy as np
import tensorflow as tf
from keras.applications.resnet50 import preprocess_input
from ultralytics import YOLO
import cv2
import easyocr

# Paths to models and data
database_path = "database.json"
Classification_model_path = r"/home/rahul/Desktop/trained models/Classification_model.h5"
license_model_path = r"/home/rahul/Desktop/trained models/License_model.pt"
citizenship_model_path = r"/home/rahul/Desktop/trained models/Citizenship_model.pt"
passport_model_path = r"/home/rahul/Desktop/trained models/withoutdocumenttype_Passport_model.pt"

# Load models
classification_model = tf.keras.models.load_model(Classification_model_path)
license_model = YOLO(license_model_path)
citizenship_model = YOLO(citizenship_model_path)
passport_model = YOLO(passport_model_path)

# Map the output class indices to document types
class_mapping_for_classification = {
    0: 'Citizenship',
    1: 'License',
    2: 'Passport',
    3: 'Other documents'
}

# Map YOLO class indices to text labels for each document type
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

# Correct the image orientation if necessary based on EXIF metadata
def correct_image_orientation(uploaded_file):
    image = Image.open(uploaded_file)
    image = ImageOps.exif_transpose(image)  # Corrects for camera rotation
    return image

st.markdown("<h1 style='text-align: center;'>Document and Record Management</h1>", unsafe_allow_html=True)
st.write("You can either use webcam to upload an image or upload a scanned image.")

uploaded_image = st.file_uploader("Choose an image", type=['png', 'jpg'])

# If an image is uploaded, process it
if uploaded_image:
    st.write("Image uploaded")
    
    # Correct the image orientation and convert it to RGB format
    img = correct_image_orientation(uploaded_image)
    img = img.convert('RGB')
    img_array = np.array(img)

    # Resize the image for input into the classification model
    img_resized = cv2.resize(img_array, (500, 500))
    img_expanded = np.expand_dims(img_resized, axis=0)
    img_preprocessed = preprocess_input(img_expanded)  # Preprocess for ResNet50

    # Predict the document type using the classification model
    predictions = classification_model.predict(img_preprocessed)
    predicted_class_index = np.argmax(predictions, axis=1)[0]
    confidence = np.max(predictions)

    predicted_class_label = class_mapping_for_classification[predicted_class_index]
    st.write('Predicted class: ' + predicted_class_label)
    st.write('Confidence: ' + str(confidence))

    # Convert image to grayscale and then back to BGR
    img_gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    img_bgr = cv2.cvtColor(img_gray, cv2.COLOR_GRAY2BGR)

    # Initialize OCR for text extraction
    ocr = easyocr.Reader(["en"])
    
    if predicted_class_label == "License":
        st.write("Processing License document...")
        results = license_model(img_bgr)
        
    elif predicted_class_label == "Citizenship":
        st.write("Processing Citizenship document...")
        results = citizenship_model(img_bgr)
        ocr = easyocr.Reader(["ne"])
        
    elif predicted_class_label == "Passport":
        st.write("Processing Passport document...")
        results = passport_model(img_bgr)
        ocr = easyocr.Reader(["ne", "en"])
        
    else:
        st.write('Document type not supported for detailed processing.')
        st.image(img_array, caption="Original Image")
        st.stop()

    collected_texts = {label: [] for label in class_mappings[predicted_class_label].values()}
    highest_conf_boxes = {}

    # Loop through the YOLO detection results
    for result in results:
        if result.boxes is not None:
            boxes = result.boxes.xyxy.cpu().numpy()
            class_ids = result.boxes.cls.cpu().numpy()
            confidences = result.boxes.conf.cpu().numpy()

            for i in range(len(class_ids)):
                class_id = int(class_ids[i])
                confidence = confidences[i]
                x1, y1, x2, y2 = map(int, boxes[i].tolist())
                label = class_mappings[predicted_class_label].get(class_id, "Unknown")

                if label not in highest_conf_boxes or confidence > highest_conf_boxes[label][1]:
                    highest_conf_boxes[label] = [(x1, y1, x2, y2), confidence]

    # Image dimensions for cropping
    height, width = img_bgr.shape[:2]

    for label, (box, confidence) in highest_conf_boxes.items():
        x1, y1, x2, y2 = box

        # Ensure coordinates are within image bounds
        x1 = max(0, x1)
        y1 = max(0, y1)
        x2 = min(width, x2)
        y2 = min(height, y2)

        # Crop from the original image (img_array), not the BGR image
        cropped_img = img_array[y1:y2, x1:x2]

        # Check if the cropped image is not empty
        if cropped_img.size == 0:
            st.write(f"Warning: Cropped image for {label} is empty.")
            continue

        ocr_result = ocr.readtext(cropped_img)

        for detection in ocr_result:
            text = detection[1]
            collected_texts[label].append(text)

        color = (255, 0, 0)
        font_scale = 1.2
        font_thickness = 2

        # Draw rectangles and labels on the BGR image for visualization
        cv2.rectangle(img_bgr, (x1, y1), (x2, y2), color, 2)
        cv2.putText(img_bgr, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, font_thickness)


    st.image(cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB), caption="Processed Image")

    st.write("Extracted Texts:")
    with open(database_path, "w") as db:
        for label, texts in collected_texts.items():
            st.write(f"{label}: {' '.join(texts)}")
