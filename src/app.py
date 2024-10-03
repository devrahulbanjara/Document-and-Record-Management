import streamlit as st
from process_image import process_image

st.set_page_config(page_title="Document and Record Management", page_icon="📝", layout="wide")

st.markdown(
    """
    <style>
    .reportview-container {
        background-size: cover;
    }
    body {
        background-color: #e8f0fe;
    }
    .title {
        text-align: center;
        font-size: 36px;
        color: #1E90FF;
        font-weight: bold;
        margin: 20px 0;
    }
    .subtitle {
        text-align: center;
        font-size: 24px;
        color: #4B0082;
        margin: 10px 0;
    }
    .button {
        display: block;
        margin: 20px auto;
        background-color: #1E90FF;
        color: white;
        padding: 10px 20px;
        border-radius: 5px;
        text-align: center;
        font-size: 16px;
        border: none;
        cursor: pointer;
    }
    .button:hover {
        background-color: #00BFFF;
    }
    .footer {
        text-align: center;
        font-size: 12px;
        color: #888888;
        margin-top: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<h1 class='title'>Document and Record Management</h1>", unsafe_allow_html=True)
st.markdown("<h2 class='subtitle'>Upload or Capture a Document for Verification</h2>", unsafe_allow_html=True)

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

st.markdown("<div class='footer'>Made with ♡ by Rahul Dev Banjara</div>", unsafe_allow_html=True)
