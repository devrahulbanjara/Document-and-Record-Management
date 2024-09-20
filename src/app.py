import streamlit as st
from PIL import Image, ImageOps
import numpy as np
from keras.applications.resnet50 import preprocess_input
import cv2
from classification import classify_image
from detection import detector
from ocrtext import perform_ocr
from database import insert_passport, insert_license, insert_citizenship, citizenship_exists, doc_info_exists

database_path = "database.json"

def correct_image_orientation(uploaded_file):
    image = Image.open(uploaded_file)
    image = ImageOps.exif_transpose(image)
    return image

st.markdown("<h1 style='text-align: center;'>Document and Record Management</h1>", unsafe_allow_html=True)
st.write("You can either use webcam to upload an image or upload a scanned image.")

uploaded_image = st.file_uploader("Choose an image", type=['png', 'jpg'])

if uploaded_image:
    st.write("Image uploaded")
    
    img = correct_image_orientation(uploaded_image)
    img = img.convert('RGB')
    img_array = np.array(img)

    img_resized = cv2.resize(img_array, (500, 500))
    img_expanded = np.expand_dims(img_resized, axis=0)
    img_preprocessed = preprocess_input(img_expanded)

    predicted_class_label,confidence = classify_image(img_preprocessed)
    
    st.write('Predicted class: ' + predicted_class_label + ' with confidence: ' + str(confidence))

    if predicted_class_label == "Other documents":
        st.warning('Document type not supported for checking in the database.')
        st.stop()
    else:
    # Convert image to grayscale and then back to BGR
        img_gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        img_bgr = cv2.cvtColor(img_gray, cv2.COLOR_GRAY2BGR)
        height, width = img_bgr.shape[:2]

        highest_conf_boxes, ocr , collected_texts = detector(predicted_class_label, img_bgr)

        perform_ocr(highest_conf_boxes, ocr,predicted_class_label, collected_texts, img_array, img_bgr)

        st.image(cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB), caption="Processed document image")

        # st.write("Extracted Texts:")
        with open(database_path, "w") as db:
            for label, texts in collected_texts.items():
                st.write(f"{label}: {' '.join(texts)}")

        # name = "Aayush"
        # surname = "Neupane"
        # dob = "2006-04-06"
        # passport_number = "1234"
        # contact_number = "9876543232"
        # district = "Nuwakot"
        # gender = "Male"
        # citizenship_number = "12345"
        
        # if citizenship_exists(citizenship_number):
        #     if not doc_info_exists(predicted_class_label, citizenship_number):
        #         if predicted_class_label == "Passport":
        #             insert_passport(name, surname, dob, citizenship_number, passport_number)
        #         elif predicted_class_label == "Citizenship":
        #             insert_citizenship(name, district, dob, citizenship_number, gender)
        #         elif predicted_class_label == "License":
        #             insert_license(name, contact_number, dob, citizenship_number, passport_number)
        #         st.write("Successfully inserted " + predicted_class_label + " of " + name + " to the database.")
        #     else:
        #         st.warning("This person already has " + predicted_class_label + " info in the database.")            
        # else:
        #     st.warning("The person with citizenship number does not exist in the database.")

