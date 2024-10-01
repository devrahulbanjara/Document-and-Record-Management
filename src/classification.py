import numpy as np
import tensorflow as tf

class_mapping_for_classification = {
    0: 'Citizenship',
    1: 'License',
    2: 'Passport',
    3: 'Other documents'
}

def classify_image(img_preprocessed):
    model_path= "../trained models/Classification_model.h5"
    classification_model = tf.keras.models.load_model(model_path)
    predictions = classification_model.predict(img_preprocessed)
    predicted_class_index = np.argmax(predictions, axis=1)[0]
    confidence = np.max(predictions)
    predicted_class_label = class_mapping_for_classification[predicted_class_index]
    return predicted_class_label, confidence
