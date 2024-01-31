# DeepFake_Detector

## Building a deep fake image detection model that is capable of classifying images into two categories Ai-Generated or Real images using TensorFlow

# Problem Definition
* The model is used for the detection of deep fake or AI-generated images that 
  are now widely used for spreading hate speech and fake news.

# Data
* We are using Kaggle data  uploaded on the drive and will also upload    a zip file on GitHub
* For the Training dataset our project includes 37,900 Fake and 10,000 Real images which can create a bias so our project acknowledges these issues by reducing the number of fake images without affecting the accuracy largely


# Evaluation

* Prediction Probabilities should be more than 90% which is this project's goal to achieve

# Features

* A few key information about features as the project is based on unstructured image classification, Thus there is no such distinctive feature but the data is divided into 3 parts. Testing, Training, and Validation. the model will be a binary classifier

``# for unzipping the zip file run this
#!unzip '/content/drive/MyDrive/Deepfake/deepfake.zip' -d "/content/drive/MyDrive/Deepfake/"``
