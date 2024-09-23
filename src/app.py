import streamlit as st
from PIL import Image, ImageOps
import numpy as np
from keras.applications.resnet50 import preprocess_input
import cv2
from classification import classify_image
from detection import detector
from ocrtext import perform_ocr
from database import check_citizenship_number,check_document
from filter_citizenship import filter_citizenship_details
from filter_license import filter_license_details
from filter_passport import filter_passport_details

database_path = "database.json"

def correct_image_orientation(uploaded_file):
    image = Image.open(uploaded_file)
    image = ImageOps.exif_transpose(image)
    return image

st.markdown("<h1 style='text-align: center;'>Document and Record Management</h1>", unsafe_allow_html=True)
st.write("You can either use webcam to upload an image or upload a scanned image.")

uploaded_image = st.file_uploader("Choose an image", type=['png', 'jpg'])

if uploaded_image:
    
    img = correct_image_orientation(uploaded_image)
    img = img.convert('RGB')
    img_array = np.array(img)

    img_resized = cv2.resize(img_array, (500, 500))
    img_expanded = np.expand_dims(img_resized, axis=0)
    img_preprocessed = preprocess_input(img_expanded)

    predicted_class_label,confidence = classify_image(img_preprocessed)
    
    st.write('The document is : ' + predicted_class_label )
    st.write('Confidence: ' + str(confidence))

    if predicted_class_label == "Other documents":
        st.warning('Document type not supported for checking in the database.')
        st.stop()
    else:
        img_gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        img_bgr = cv2.cvtColor(img_gray, cv2.COLOR_GRAY2BGR)
                
        highest_conf_boxes, ocr , collected_texts = detector(predicted_class_label, img_bgr)

        collected_texts = perform_ocr(highest_conf_boxes, ocr,predicted_class_label, collected_texts, img_array, img_bgr)

        st.image(cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB), caption="Provided document image")
                    
        print("Non filtered    " + str(list(collected_texts.values())))
               
        if predicted_class_label == "Citizenship":
            details = filter_citizenship_details(collected_texts)
            
            st.write()
            
            exists = check_citizenship_number(details["citizenship_number"],details["name"])
            if not exists:
                st.warning("The given citizenship number doesn't exist.")
                print(f"No match found")

            else:
                st.warning("This is a genuine "+predicted_class_label)
                print(f"80% match found")
                
            print("Filtered    " + str(list(details.values())))

        elif predicted_class_label == "License":
            details = filter_license_details(collected_texts)
            
            st.write()
            
            exists = check_citizenship_number(details["citizenship_number"],details["name"])
            if not exists:
                st.warning("The ctizenship number doesnt exist which is given in the license.")
                
            check_document(details["citizenship_number"],details["license_number"],predicted_class_label)
            
            print("Filtered    " + str(list(details.values())))

            
        elif predicted_class_label == "Passport":
            details = filter_passport_details(collected_texts)
            
            st.write()
            exists = check_citizenship_number(details["citizenship_number"],details["name"])
            if not exists:
                st.warning("The ctizenship number doesnt exist which is given in the passport.")
                
            check_document(details["citizenship_number"],details["passport_number"],predicted_class_label)

            
            print("Filtered    " + str(list(details.values())))

