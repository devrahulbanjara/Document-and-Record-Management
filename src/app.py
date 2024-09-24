import streamlit as st
from PIL import Image, ImageOps
import numpy as np
from keras.applications.resnet50 import preprocess_input
import cv2
from classification import classify_image
from detection import detector
from ocrtext import perform_ocr
from database import citizenship_number_exists, document_key_exists, name_matches, date_matches, doc_number_matches
from filter_citizenship import filter_citizenship_details
from filter_license import filter_license_details
from filter_passport import filter_passport_details

st.markdown("<h1 style='text-align: center;'>Document and Record Management</h1>", unsafe_allow_html=True)
st.write("You can either use webcam to upload an image or upload a scanned image.")

def correct_image_orientation(uploaded_file):
    image = Image.open(uploaded_file)
    image = ImageOps.exif_transpose(image)
    return image

def validate_document(details, document_type, document_number_key):
    if citizenship_number_exists(details["citizenship_number"]):
        if document_key_exists(details["citizenship_number"], details[document_number_key], document_type):
            if doc_number_matches(details[document_number_key], details["citizenship_number"], document_type):
                if date_matches(details["dob"], details["citizenship_number"], document_type):
                    st.warning(f"Genuine {document_type}")
                else:
                    st.warning(f"The extracted {document_type} DOB doesn't match with the {document_type} DOB in the JSON.")
            else:
                st.warning(f"The {document_type} number does not match to the one in the database.")
        else:
            st.warning(f"The given person has no {document_type.lower()} registered.")
    else:
        st.warning(f"The citizenship number which is in the {document_type} doesn't exist.")


uploaded_image = st.file_uploader("Choose an image", type=['png', 'jpg'])

if uploaded_image:
    
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
        print()
        print()
        print("Non filtered ",end=" ")
        print(collected_texts)
               
        if predicted_class_label == "Citizenship":
            details = filter_citizenship_details(collected_texts)
            print("Filtered Data ",end=" ")
            print(details)
            if citizenship_number_exists(details["citizenship_number"]):
                if name_matches(details["name"]) and date_matches(details["year_of_birth"], details["citizenship_number"], "Citizenship"):
                    st.warning("Genuine citizenship.")
                else:
                    st.warning("Citizenship number exists but the details do not match.")
            else:
                st.warning("The given citizenship number doesn't exist.")
                print("Extracted citizenship number doesn't match with the one in the json.")

        if predicted_class_label == "License":
            details = filter_license_details(collected_texts)
            print("Filtered Data ",end=" ")
            print(details)
            validate_document(details, "License", "license_number")
    
        elif predicted_class_label == "Passport":
            details = filter_passport_details(collected_texts)
            print("Filtered Data ",end=" ")
            print(details)
            validate_document(details, "Passport", "passport_number")
