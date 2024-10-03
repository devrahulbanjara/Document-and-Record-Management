import streamlit as st
from PIL import Image
import numpy as np
import cv2
from keras.applications.resnet50 import preprocess_input
from classification import classify_image
from detection import detector
from ocrtext import perform_ocr
from filter_citizenship import filter_citizenship_details
from filter_license import filter_license_details
from filter_passport import filter_passport_details
from validate_document import validate_document
from validate_citizenship import validate_citizenship
from image_orientation import correct_image_orientation
from plot_details import plot_citizenship, plot_license, plot_passport
from database import person_info

def process_image(uploaded_image):
    img = correct_image_orientation(uploaded_image)
    img = img.convert('RGB')
    img_array = np.array(img)

    img_resized = cv2.resize(img_array, (500, 500))
    img_expanded = np.expand_dims(img_resized, axis=0)
    img_preprocessed = preprocess_input(img_expanded)

    predicted_class_label, confidence = classify_image(img_preprocessed)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center; color: #1E90FF;'>{predicted_class_label} detected</h3>", unsafe_allow_html=True)
    st.markdown(f"<h6 style='text-align: center; color: #1E90FF;'>{round(confidence * 100, 2)}%</h6>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    if predicted_class_label == "Other documents":
        st.warning('Document type not supported for checking in the database.')
        st.stop()

    img_gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    img_bgr = cv2.cvtColor(img_gray, cv2.COLOR_GRAY2BGR)

    highest_conf_boxes, ocr, collected_texts = detector(predicted_class_label, img_bgr)
    collected_texts = perform_ocr(highest_conf_boxes, ocr, predicted_class_label, collected_texts, img_array, img_bgr)

    error_message = None
    success_message = None
    details = {}

    if predicted_class_label == "Citizenship":
        details = filter_citizenship_details(collected_texts)
        is_genuine = validate_citizenship(details)
        if isinstance(is_genuine, str):
            error_message = is_genuine
        elif is_genuine:
            details = person_info(details["citizenship_number"], "Citizenship")
            success_message = "Genuine Citizenship"

    elif predicted_class_label == "License":
        details = filter_license_details(collected_texts)
        is_genuine = validate_document(details, "License", "license_number")
        if isinstance(is_genuine, str):
            error_message = is_genuine
        elif is_genuine:
            details = person_info(details["citizenship_number"], "License")
            success_message = "Genuine License"

    elif predicted_class_label == "Passport":
        details = filter_passport_details(collected_texts)
        is_genuine = validate_document(details, "Passport", "passport_number")
        if isinstance(is_genuine, str):
            error_message = is_genuine
        elif is_genuine:
            details = person_info(details["citizenship_number"], "Passport")
            success_message = "Genuine Passport"

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div class='image-container'>", unsafe_allow_html=True)
        st.image(cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB), caption="Provided Document Image", use_column_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        if predicted_class_label == "Citizenship":
            plot_citizenship(details, is_genuine)
        elif predicted_class_label == "License":
            plot_license(details)
        elif predicted_class_label == "Passport":
            plot_passport(details)

    if success_message:
        st.markdown(f"<h2 style='text-align: center; color: green;'>{success_message}</h3>", unsafe_allow_html=True)
    elif error_message:
        st.error(error_message)
        st.markdown(f"<h3 style='text-align: center; color: #DC3545;'>❌ Fraudulent {predicted_class_label}</h3>", unsafe_allow_html=True)
