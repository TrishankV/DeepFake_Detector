from flask import Flask, render_template, request
import numpy as np
import tensorflow as tf
# from tensorflow import load_model
from PIL import Image
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
MODEL_PATH = 'C:\\Users\\vedant\\OneDrive\\Desktop\\Deepfake\\model\\my_model_1.h5'

# Load the pre-trained model
model = new_model = tf.keras.models.load_model(MODEL_PATH)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
        uploaded_file.save(file_path)
        prediction = process_image(file_path)
        return render_template('index.html', image=file_path, prediction=prediction)
    return render_template('index.html')

def process_image(file_path):
    # Open and preprocess the image
    image = tf.io.read_file(file_path)
    # Example: Resize the image to fit model input size
    image = tf.image.decode_jpeg(image,channels = 3)
    image = tf.image.convert_image_dtype(image,tf.float32)#normalize
    image = tf.image.resize(image,size=[224,224])
    # Example: Convert image to numpy array
    img_array = np.array(image) 
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension

    # Example: Make predictions using the loaded model
    predictions = model.predict(img_array)

    # Example: Convert predictions to human-readable format
    # Replace this with your actual post-processing code
    threshold = 0.5

# Categorize the prediction
    if predictions >= threshold:
        prediction_class = 'Real_Image'
    else:
        prediction_class = 'Ai-generated Image'

    prediction_label = f'{prediction_class}'

    return prediction_label

if __name__ == '__main__':
    app.run(debug=True)
