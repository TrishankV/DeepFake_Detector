# DeepFake_Detector

## Building a deep fake image detection model that is capable of classifying images into two categories Ai-Generated or Real images using TensorFlow

# Problem Definition
* The model is used for the detection of deep fake or AI-generated images that 
  are now widely used for spreading hate speech and fake news.

# Data
*We are using Kaggle data  uploaded on the drive can be downloaded from the following URL
https://www.kaggle.com/datasets/ericji150/nsf-reu-2023-sd-21
[E. Ji, B. Dong, B. Samanthula, N. Zhou. "2D-FACT: Dual-Domain Fake Image Detection Against Textto-Image Generative Models". MIT Undergraduate Research Technology Conference (URTC 2023).]

* For the Training dataset our project includes 10,000 Fake and 10,000 Real images which can create a bias so our project acknowledges these issues by reducing the number of fake images without affecting the accuracy largely


# Evaluation

* Prediction Probabilities should be more than 90% which is this project's goal to achieve

  # *Resources Referred for transfer learning*
* *Kaggle models* = https://www.kaggle.com/models?tfhub-redirect=true
* *Pytorch hub* = https://pytorch.org/hub/
* *Object detection* = https://www.kaggle.com/models/google/mobilenet-v2/frameworks/tensorFlow2/variations/130-224-classification/versions/1?tfhub-redirect=true
* *Papers with code* = https://paperswithcode.com/
* *Tesla model uses RESNET-50 model* = https://www.youtube.com/watch?v=oBklltKXtDE&t=173s
* *Tensorflow hub* = https://www.tensorflow.org/resources/models-datasets
* *Model-Zoo* = https://www.modelzoo.co/  

# Features

* A few key information about features as the project is based on unstructured image classification, Thus there is no such distinctive feature but the data is divided into 3 parts. Testing, Training, and Validation. the model will be a binary classifier

``# for unzipping the zip file run this
#!unzip '/content/drive/MyDrive/Deepfake/deepfake.zip' -d "/content/drive/MyDrive/Deepfake/"``
