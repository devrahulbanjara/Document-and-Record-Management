import streamlit as st
from PIL import Image, ImageOps
import numpy as np
import cv2
from keras.applications.resnet50 import preprocess_input
from classification import classify_image
from detection import detector
from ocrtext import perform_ocr
from database import citizenship_number_exists, document_key_exists, name_matches, date_matches, doc_number_matches
from filter_citizenship import filter_citizenship_details
from filter_license import filter_license_details
from filter_passport import filter_passport_details

st.markdown("<h1 style='text-align: center; color: #FF6347;'>Document and Record Management System</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #2E8B57;'>Capture or Upload a Document for Validation</h3>", unsafe_allow_html=True)

def correct_image_orientation(uploaded_file):
    image = Image.open(uploaded_file)
    image = ImageOps.exif_transpose(image)
    return image

def validate_document(details, document_type, document_number_key):
    stored_citizenship_number, number_exists = citizenship_number_exists(details["citizenship_number"])

    if number_exists:
        if document_key_exists(stored_citizenship_number, details[document_number_key], document_type):
            if doc_number_matches(details[document_number_key], stored_citizenship_number, document_type):
                if date_matches(details["dob"], stored_citizenship_number, document_type):
                    st.warning(f"✅ Genuine {document_type}")
                else:
                    st.error(f"❌ The extracted {document_type} DOB doesn't match with the {document_type} DOB in the JSON.")
            else:
                st.error(f"❌ The {document_type} number does not match the one in the database.")
        else:
            st.error(f"❌ The given person has no {document_type.lower()} registered.")
    else:
        st.error(f"❌ The citizenship number which is in the {document_type} doesn't exist.")

def process_image(uploaded_image):
    img = correct_image_orientation(uploaded_image)
    img = img.convert('RGB')
    img_array = np.array(img)

    img_resized = cv2.resize(img_array, (500, 500))
    img_expanded = np.expand_dims(img_resized, axis=0)
    img_preprocessed = preprocess_input(img_expanded)

    predicted_class_label, confidence = classify_image(img_preprocessed)
    
    st.write('The document is : ' + predicted_class_label)
    st.write('Confidence: ' + str(confidence))

    if predicted_class_label == "Other documents":
        st.warning('Document type not supported for checking in the database.')
        st.stop()
    else:
        img_gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        img_bgr = cv2.cvtColor(img_gray, cv2.COLOR_GRAY2BGR)
                
        highest_conf_boxes, ocr, collected_texts = detector(predicted_class_label, img_bgr)

        collected_texts = perform_ocr(highest_conf_boxes, ocr, predicted_class_label, collected_texts, img_array, img_bgr)

        st.image(cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB), caption="Provided document image")

        print("\nNon filtered Data ", collected_texts)
               
        if predicted_class_label == "Citizenship":
            details = filter_citizenship_details(collected_texts)
            print("\nFiltered Data ", details)
            
            stored_citizenship_number, number_exists = citizenship_number_exists(details["citizenship_number"])

            if number_exists:
                if date_matches(details["year_of_birth"], stored_citizenship_number, "Citizenship"):
                    if name_matches(details["name"]):
                        st.warning("✅ Genuine citizenship.")
                    else:
                        st.error("❌ Citizenship number exists, but the name doesn't match.")
                else:
                    st.error("❌ Citizenship number exists, but the date doesn't match.")
            else:
                st.error("❌ The given citizenship number doesn't exist.")

        elif predicted_class_label == "License":
            details = filter_license_details(collected_texts)
            print("\n Filtered Data ", details)
            validate_document(details, "License", "license_number")
    
        elif predicted_class_label == "Passport":
            details = filter_passport_details(collected_texts)
            print("\n Filtered Data ", details)
            validate_document(details, "Passport", "passport_number")

option = st.selectbox("Choose your input method", ("Upload Image", "Use Webcam"))

if option == "Upload Image":
    uploaded_image = st.file_uploader("Upload a document image (png or jpg)", type=['png', 'jpg'])
    if uploaded_image:
        process_image(uploaded_image)

elif option == "Use Webcam":
    picture = st.camera_input("Take a picture") 
    if picture:
        process_image(picture)
    else:
        st.warning("⚠️ No image captured. Please take a photo.")
