from flask import Flask, flash , render_template, request, redirect, url_for , send_from_directory
import numpy as np
import tensorflow as tf
from werkzeug.utils import secure_filename
from PIL import Image ,ImageDraw,ImageFont
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
MODEL_PATH = r'my_model_1.h5'
# MODEL_PATH = r'C://Users//vedant//Downloads//DF//DeepFake_Detector-main//Flask_application//my_model_1.h5'
app.secret_key = "Argentavious"
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

# @app.route('/upload', methods=['POST'])
# def upload_file():
#     os.makedirs(UPLOAD_FOLDER, exist_ok=True)
#     uploaded_file = request.files['file']
#     filename = secure_filename(uploaded_file.filename)
#     print(filename)
#     if uploaded_file.filename != '':
#         file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
#         img_path = os.path.join('static/images', uploaded_file.filename)
#         uploaded_file.save(file_path)
#         uploaded_file.save(img_path)
        
#         flash('Image successfully uploaded')
#         prediction = process_image(file_path)
#         return render_template('uploaded_file.html', filename=filename,prediction=prediction)
#     return render_template('index.html')
# 
@app.route('/upload', methods=['POST'])
def upload_file():
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if uploaded_file.filename != '':
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        img_path = os.path.join('static/images', filename)
        uploaded_file.save(file_path)
        uploaded_file.save(img_path)
        
        flash('Image successfully uploaded')
        prediction = process_image(file_path)
        # Apply watermark
        wm_image_path = apply_watermark(file_path, prediction)
        print(wm_image_path,filename)
        
        # watermark image file alteration
        # filename = wm_image_path.split("uploads")[1]
        # filename = filename[1:]
        # print(filename)
        # shoud download on click 

        return render_template('uploaded_file.html', filename=filename, prediction=prediction, wm_image_path=wm_image_path)
    
    else:
        flash('Invalid file format')
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

def apply_watermark(input_image_path, watermark_text):
    # Open the input image
    image = Image.open(input_image_path)
    # Apply watermark
    draw = ImageDraw.Draw(image)
    w  = image.size[0]
    h = image.size[1]
    # Define the position to place the text (top left corner)
    text_x = 0
    text_y = 0
    
    # Define the size of the rectangle
    rectangle_width = w/4  # Adjust as needed
    rectangle_height = 45  # Adjust as needed
    
    # Draw the semi-transparent black container at the top left corner
    rectangle_x = text_x
    rectangle_y = text_y
    draw.rectangle([rectangle_x, rectangle_y, rectangle_x + rectangle_width, rectangle_y + rectangle_height], fill=(0, 0, 0, 128))

    font = ImageFont.truetype("arial.ttf", 30)
    draw.text((10, 10), watermark_text, fill=(255, 255, 255, 128), font=font)
    
    # Save the watermarked image
    wm_image_path = os.path.join(os.path.dirname(input_image_path), "watermarked_" + os.path.basename(input_image_path))
    image.save(wm_image_path)
    
    return wm_image_path
# def apply_watermark(input_image_path, watermark_text):
#     # Open the input image
#     image = Image.open(input_image_path)
    
#     # Apply watermark
#     draw = ImageDraw.Draw(image)
#     width, height = image.size
#     font = ImageFont.truetype("arial.ttf", 30)
#     text_width, text_height = draw.textsize(watermark_text, font=font)
    
#     # Define the rectangle for the semi-transparent black container
#     rectangle_width = text_width + 20
#     rectangle_height = text_height + 10
#     rectangle_x = width - rectangle_width - 10
#     rectangle_y = height - rectangle_height - 10
    
#     # Draw the semi-transparent black container
#     draw.rectangle([rectangle_x, rectangle_y, width, height], fill=(0, 0, 0, 128))
    
#     # Draw the text on top of the container
#     text_x = rectangle_x + 10
#     text_y = rectangle_y + 5
#     draw.text((text_x, text_y), watermark_text, fill=(255, 255, 255), font=font)
    
#     # Save the watermarked image
#     wm_image_path = os.path.join(os.path.dirname(input_image_path), "watermarked_" + os.path.basename(input_image_path))
#     image.save(wm_image_path)
    
#     return wm_image_path

if __name__ == '__main__':
    app.run(debug=True)
