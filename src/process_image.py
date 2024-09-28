import streamlit as st
from PIL import Image, ImageOps, ImageDraw, ImageFont
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
from plot_details import draw_citizenship_details, draw_license_details, draw_passport_details
from database import person_info

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

    img_gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    img_bgr = cv2.cvtColor(img_gray, cv2.COLOR_GRAY2BGR)

    highest_conf_boxes, ocr, collected_texts = detector(predicted_class_label, img_bgr)
    collected_texts = perform_ocr(highest_conf_boxes, ocr, predicted_class_label, collected_texts, img_array, img_bgr)

    print("\nNon filtered Data ", collected_texts)

    blank_image_pil = Image.new('RGB', (400, 300), color=(255, 255, 255))
    draw = ImageDraw.Draw(blank_image_pil)

    standard_font_size = int(400 * 0.05)
    default_font = ImageFont.truetype("DejaVuSans.ttf", standard_font_size)
    nepali_font = ImageFont.truetype("mangal.ttf", standard_font_size)

    if predicted_class_label == "Citizenship":
        details = filter_citizenship_details(collected_texts)
        print("\nFiltered Data ", details)

        is_genuine = validate_citizenship(details)
        if is_genuine:
            details = person_info(details["citizenship_number"],"Citizenship")
        draw_citizenship_details(draw, details, nepali_font,is_genuine)

    elif predicted_class_label == "License":
        details = filter_license_details(collected_texts)
        print("\nFiltered Data ", details)
        
        is_genuine = validate_document(details, "License", "license_number")
        if is_genuine:
            details = person_info(details["citizenship_number"],"License")
        draw_license_details(draw, details, default_font)

    elif predicted_class_label == "Passport":
        details = filter_passport_details(collected_texts)
        print("\nFiltered Data ", details)

        is_genuine = validate_document(details, "Passport", "passport_number")
        if is_genuine:
            details = person_info(details["citizenship_number"],"Passport")
        draw_passport_details(draw, details, default_font)

    blank_image_np = np.array(blank_image_pil)

    display_img_bgr = cv2.resize(img_bgr, (500, 500))
    display_blank_img = cv2.resize(blank_image_np, (500, 500))

    col1, col2 = st.columns(2)
    with col1:
        st.image(cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB), caption="Provided document image")

    with col2:
        st.image(blank_image_np, caption="Extracted Information")
