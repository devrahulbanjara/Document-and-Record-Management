import streamlit as st
from PIL import Image
import numpy as np 
import torch
import tensorflow as tf
import os
from tensorflow.keras.preprocessing import image
from keras.applications.resnet50 import preprocess_input

Classification_model_path = "/mnt/c/Users/Rahul/Desktop/trained models/Classification_model.h5"
classification_model = tf.keras.models.load_model(Classification_model_path)

st.write("Document and Record Management")
st.write("Please insert a document image (Citizenship, Driving License or Passport)")

uploaded_image = st.file_uploader("Choose an image", type=['png', 'jpg'])

if uploaded_image:
    st.write("Image uploaded")
    img = image.load_img(uploaded_image, target_size=(500, 500))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

    class_mapping = {
        0: 'citizenship',
        1: 'license',
        2: 'passport',
        3: 'others'
    }

    predictions = classification_model.predict(img_array)
    predicted_class_index = np.argmax(predictions, axis=1)[0]
    confidence = np.max(predictions)

    predicted_class_label = class_mapping[predicted_class_index]
    st.write('Predicted class: ' + predicted_class_label)
    st.write('Confidence: ' + str(confidence))
