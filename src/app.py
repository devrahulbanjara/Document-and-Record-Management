import streamlit as st
from process_image import process_image

st.markdown("<h1 style='text-align: center; color: #FF6347;'>Document and Record Management System</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #2E8B57;'>Capture or Upload a Document for Validation</h3>", unsafe_allow_html=True)

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