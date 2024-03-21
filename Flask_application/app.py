from flask import Flask, flash , render_template, request, redirect, url_for , send_from_directory,send_file
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
        print(f'wm:{wm_image_path},file{filename}')
        
        # watermark image file alteration
        wm_image_path = wm_image_path.split("uploads")[1]
        wm_image_path = wm_image_path[1:]
        print(wm_image_path)
        # shoud download on click 

        return render_template('uploaded_file.html', filename=filename, prediction=prediction, wm_image_path=wm_image_path)
    
    else:
        flash('Invalid file format')
        return render_template('index.html')
    
@app.route('/download_image', methods=['GET', 'POST'])
def download_file():
    filename = request.args.get('filename')
    if request.method == 'GET':
        # Handle GET request for downloading file
        # This part remains the same as before
        filename = request.args.get('filename')

    elif request.method == 'POST':
        # Handle POST request for downloading file
        # Get the file type and aspect ratio from the form data
        file_type = request.form.get('file_type', 'png')  # Default to png if not specified
        aspect_ratio = request.form.get('aspect_ratio', 'original')  # Default to original if not specified

        try:
            # Construct the complete file path
            static_folder_path = app.static_folder  # Get the path to the static folder
            print(static_folder_path)
            original_filename = filename  # Specify the filename without extension
            print(original_filename)
            filename_without_extension = original_filename.split('.')[0]  # Extract filename without extension
            print(filename_without_extension)
            file_path = os.path.join(static_folder_path, 'uploads/', filename_without_extension + '.' + file_type)
            file_path = file_path.replace("\\", "/")
            # Check if the file exists
            if os.path.exists(file_path):
                # If the file exists, return it
                return send_file(file_path, as_attachment=True)
            else:
                # If the file does not exist, return a 404 error
                return 'File not found', 404
        except Exception as e:
            # Log any exceptions that occur during processing
            print(f"Error occurred during file download: {e}")
            return 'Internal Server Error', 500
    
# @app.route('/uploads/<filename>')
# def uploaded_file(filename):
#     file_path = os.path.join(UPLOAD_FOLDER, filename)
#     prediction = process_image(file_path)
#     return render_template('uploaded_file.html', image=file_path, prediction=prediction)

    
def process_image(file_path):
    # Open and preprocess the image
    image = tf.io.read_file(file_path)
    # Example: Resize the image to fit model input size
    image = image.convert("RGB")
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

# def apply_watermark(input_image_path, watermark_text):
#     # Open the input image
#     image = Image.open(input_image_path)
#     # Apply watermark
#     draw = ImageDraw.Draw(image)
#     w  = image.size[0]
#     h = image.size[1]
#     # Define the position to place the text (top left corner)
#     text_x = 0
#     text_y = 0
    
#     # Define the size of the rectangle
#     rectangle_width = w/4  # Adjust as needed
#     rectangle_height = 45  # Adjust as needed
    
#     # Draw the semi-transparent black container at the top left corner
#     rectangle_x = text_x
#     rectangle_y = text_y
#     draw.rectangle([rectangle_x, rectangle_y, rectangle_x + rectangle_width, rectangle_y + rectangle_height], fill=(0, 0, 0, 128))

#     font = ImageFont.truetype("arial.ttf", 30)
#     draw.text((10, 10), watermark_text, fill=(255, 255, 255, 128), font=font)
    
#     # Save the watermarked image
#     wm_image_path = os.path.join(os.path.dirname(input_image_path), "watermarked_" + os.path.basename(input_image_path))
#     image.save(wm_image_path)
    
#     return wm_image_path

def apply_watermark(input_image_path, watermark_text):
    # Open the input image
    image = Image.open(input_image_path)
    
    # Get the original width and height
    original_width, original_height = image.size
    
    # Calculate the proportional height based on the new width of 500 pixels
    new_width = 500
    new_height = int((original_height / original_width) * new_width)
    
    # Resize the image while maintaining the aspect ratio
    image = image.resize((new_width, new_height))
    
    # Apply watermark
    draw = ImageDraw.Draw(image)
    
    # Define the position to place the text (top left corner)
    text_x = 0
    text_y = 0
    
    # Define the size of the rectangle
    rectangle_width = new_width # Adjust as needed
    rectangle_height = 45  # Adjust as needed
    
    # Draw the semi-transparent black container at the top left corner
    rectangle_x = text_x
    rectangle_y = text_y
    draw.rectangle([rectangle_x, rectangle_y, rectangle_x + rectangle_width, rectangle_y + rectangle_height], fill=(0, 0, 0, 128))

    font = ImageFont.truetype("arial.ttf", 30)
    draw.text((10, 10), watermark_text, fill=(255, 255, 255, 128), font=font)
    
    # Save the watermarked image
    wm_image_path = os.path.join(os.path.dirname(input_image_path), "watermarked_" + os.path.basename(input_image_path))
    image = image.resize((original_width, original_height))
    image.save(wm_image_path)
    return wm_image_path


if __name__ == '__main__':
    app.run(debug=True)
