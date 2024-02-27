# Importing all required tools
import tensorflow as tf
import tensorflow_hub as hub
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow import keras
from keras.layers import Activation, Dense
from tensorflow.keras.models import load_model

# importing local modules
import paths as paths
from img_preprocess import *
from visualize import * 
from model import * 

# For Data Structuring
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# File Handling
import os

# For image processing
from matplotlib.pyplot import imread

BATCH_SIZE = 32
IMG_SIZE = 225

#change no of images according to data
NUM_IMAGES = 20000

print("TF Version",tf.__version__)
print("TF hub version :",hub.__version__)
print("GPU available"if tf.config.list_physical_devices("GPU")else "Not Available")
try :
    p = ("Enter the entire path where you have your dataset stored :(Use // instead of /) ")
except:
    print("Enter path in proper format")


# Forming an train_info csv
file_paths,file_name = paths(f'{p}//TRAIN//FAKE')
print(len(file_paths),len(file_name))
df = pd.DataFrame(file_name, columns=['Image'])
df['Path']= file_paths
df['Class']='Fake'
df['Target']=0
file_paths,file_name = paths(f'{p}//TRAIN//REAL')
print(len(file_name))
new_data = pd.DataFrame(file_name, columns=['Image'])
new_data['Path'] = file_paths
new_data['Class'] = 'Real'
new_data['Target'] = '1'
resulting_data = pd.concat([df, new_data], ignore_index=True)
resulting_data.to_csv(f'{p}//Test_Info.csv', index=False)
del new_data

print(resulting_data['Class'].value_counts())
resulting_data = pd.read_csv(f'{p}//Test_Info.csv')

# Shuffling data
np.random.seed(69)
resulting_data = resulting_data.sample(frac=1).reset_index(drop=True)

labels = resulting_data['Target'].to_numpy()
unique = np.unique(labels)
bool_labels = [label == unique for label in labels]
# Converting bool to Tensors
print("Binary Matrix = [fake,real]")
print(labels[11000])
print(bool_labels[11000].astype(int)) # as we have only two classes

# Splitting dataset into training and validation

X = resulting_data['Path'].to_numpy()
print(X[:10],"Length :",len(X))
Y = resulting_data['Target'].to_numpy()
print(Y[:10],"Length :",len(Y))
X_train,X_val,Y_train,Y_val = train_test_split(X[:NUM_IMAGES],Y[:NUM_IMAGES],test_size=0.2,random_state=8) # Good For Expirimenting Faster Results
print(f'Xtrain length ={len(X_train)} ,Ytrain length ={len(Y_train)} ,Xval length ={len(X_val)} ,Yval length ={len(Y_val)}')


# Crating batches

get_tupple(X[10],Y[10]) #img_preprocess_module
train_data = create_data_batches(X_train,y=Y_train)
Val_data = create_data_batches(X_val,y=Y_val,valid_data = True)
print(f'train data batch {train_data.element_spec} and val data batch {Val_data}')

#visualizing a batch
train_images, train_labels = next(train_data.as_numpy_iterator())# creating or generating the bathes
print(len(train_images),len(train_labels)) #32 is the batch size
print(train_labels)
visualize_25_images(train_images, train_labels)

# Training model
image_classifier = train_model(train_data,Val_data)
image_classifier.summary()

#Save your model
try :
    name = input("Enter name of .h5 and .keras files where the model will be stored : ")
    image_classifier.save(f'{p}//{name}.keras')
    image_classifier.save(f'{p}//{name}.h5')
except :
    print("Fatal error in path the model is saved as maverick,h5 and maverick.keras")
    name = "maverick"
    image_classifier.save(f'{p}//{name}.keras')
    image_classifier.save(f'{p}//{name}.h5')



