import tensorflow as tf
IMG_SIZE = 225
def process_image(ImagePath,img_size= IMG_SIZE):
  """
  Take image file path and convert image into tensors

  """
  # Read the image file
  image = tf.io.read_file(ImagePath)

  #Turning .jpg or jpeg into tensors (R,G,B)
  image = tf.image.decode_jpeg(image,channels = 3) #(R,G,B)

  # Normalizing the image by converting range 0 - 255 to 0 - 1
  image = tf.image.convert_image_dtype(image,tf.float32)

  # Resize the image to (224,224)
  image = tf.image.resize(image,size=[img_size,img_size])


  return image

def get_tupple(image_path, label):
  """
  Takes an image file path name and the assosciated label,
  processes the image and reutrns a typle of (image, label).
  """
  image = process_image(image_path)
  return image, label



BATCH_SIZE = 32
# Create a function to turn data into batches
def create_data_batches(X, y=None, batch_size=BATCH_SIZE, valid_data=False, test_data=False):
  """
  Creates batches of data out of image (X) and label (y) pairs.
  Shuffles the data if it's training data but doesn't shuffle if it's validation data.
  Also accepts test data as input (no labels).
  """
  # If the data is a test dataset, we probably don't have have labels
  if test_data:
    print("Creating test data batches...")
    data = tf.data.Dataset.from_tensor_slices((tf.constant(X))) # only filepaths (no labels)
    data_batch = data.map(process_image).batch(BATCH_SIZE)
    return data_batch

  # If the data is a valid dataset, we don't need to shuffle it
  elif valid_data:
    print("Creating validation data batches...")
    data = tf.data.Dataset.from_tensor_slices((tf.constant(X), # filepaths
                                               tf.constant(y))) # labels
    data_batch = data.map(get_tupple).batch(BATCH_SIZE)
    return data_batch

  else:
    print("Creating training data batches...")
    # Turn filepaths and labels into Tensors
    data = tf.data.Dataset.from_tensor_slices((tf.constant(X),
                                               tf.constant(y)))
    print(tf.constant(y))
    # Shuffling pathnames and labels before mapping image processor function is faster than shuffling images
    # data = data.shuffle(buffer_size=len(X))

    # Create (image, label) tuples (this also turns the iamge path into a preprocessed image)
    data = data.map(get_tupple)

    # Turn the training data into batches
    data_batch = data.batch(BATCH_SIZE)
  return data_batch

def map_labels(label):
    """
    Maps binary labels to 'real' and 'Aigen'.
    """
    if label == 1:
        return 'Real'
    else:
        return 'Ai-Gen'