import streamlit as st
from PIL import Image, ImageOps
import numpy as np
import cv2
from keras.applications.resnet50 import preprocess_input
from classification import classify_image
from detection import detector
from ocrtext import perform_ocr
from database import citizenship_number_exists, date_matches, name_matches
from filter_citizenship import filter_citizenship_details
from filter_license import filter_license_details
from filter_passport import filter_passport_details
from validate_document import validate_document
from image_orientation import correct_image_orientation

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
