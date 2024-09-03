from ultralytics import YOLO
import matplotlib.pyplot as plt
import numpy as np
import os
import PIL
from PIL import Image
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.callbacks import Callback
import random 
from tensorflow.keras import layers
from tensorflow.python.keras.layers import Dense, Flatten
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
from sklearn.metrics import confusion_matrix
import seaborn as sns 
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.applications.resnet50 import ResNet50 
from keras.applications.resnet50 import preprocess_input
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.preprocessing import image

img_path = "/mnt/c/Users/Rahul/Desktop/Document-and-Record-Management/notebooks/YOLOv8/60330923_865705897113261_4244452931501293568_n_jpg.rf.b3570379afe5ce35b3eba1b22d52c855.jpg"
citizenship_model_path = ""

classification_model_path = '/mnt/c/Users/Rahul/Desktop/trained models/Classification_model.h5'

classification_model = tf.keras.models.load_model(classification_model_path)





img_path= "/mnt/c/Users/Rahul/Desktop/Document-and-Record-Management/notebooks/YOLOv8/license_63_png.rf.296c03a7b61304c4724dfbbb108273ef.jpg"
img = image.load_img(img_path, target_size=(500, 500))
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
print(f'Predicted class: {predicted_class_label} with confidence: {confidence:.2f}')



