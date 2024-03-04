from flask import Flask, flash , render_template, request, redirect, url_for , send_from_directory
import numpy as np
import tensorflow as tf
from werkzeug.utils import secure_filename
from PIL import Image
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
MODEL_PATH = r'my_model_1.h5'
app.secret_key = "sex key"
# Load the pre-trained model
model = new_model = tf.keras.models.load_model(MODEL_PATH)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    print(filename)
    if uploaded_file.filename != '':
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
        img_path = os.path.join('static/images', uploaded_file.filename)
        uploaded_file.save(file_path)
        uploaded_file.save(img_path)
        
        flash('Image successfully uploaded')
        prediction = process_image(file_path)
        return render_template('uploaded_file.html', filename=filename,prediction=prediction)
    return render_template('index.html')

# @app.route('/uploads/<filename>')
# def uploaded_file(filename):
#     file_path = os.path.join(UPLOAD_FOLDER, filename)
#     prediction = process_image(file_path)
#     return render_template('uploaded_file.html', image=file_path, prediction=prediction)

    
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
        prediction_class = 'A Real Image'
    else:
        prediction_class = 'An Ai-generated Image'

    prediction_label = f'{prediction_class}'

    return prediction_label

if __name__ == '__main__':
    app.run(debug=True)
