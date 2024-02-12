from google.colab import drive
drive.mount('/content/drive')

# Importing all required tools
# Importing all required tools
import tensorflow as tf
import tensorflow_hub as hub
from sklearn.model_selection import train_test_split

# For Data Structuring
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# File Handling
import os

# For image processing
from matplotlib.pyplot import imread

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

print("TF Version",tf.__version__)
print("TF hub version :",hub.__version__)
# Checking for GPU accessibility

print("GPU available"if tf.config.list_physical_devices("GPU")else "Not Available")
print('*'*100)

# To check if the image is accessible run this if an error occurs to know the root cause
# !ls '/content/drive/MyDrive/Deepfake/Ai vs Real image Detection Dataset/train/FAKE/1069 (10).jpg'
# Can be used for displaying images
Image('/content/drive/MyDrive/Deepfake/Ai vs Real image Detection Dataset/train/FAKE/1069 (10).jpg')




