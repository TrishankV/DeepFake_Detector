import matplotlib.pyplot as plt

def visualize_25_images(image, labels):
    """
    Displays 25 images from a batch with labels mapped to 'real' and 'Aigen'.
    """
    plt.figure(figsize=(10, 10))
    for i in range(25):
        ax = plt.subplot(5, 5, i + 1)  # row, column, index
        plt.imshow(image[i])
        plt.title("Label: " + map_labels(labels[i]))  # Map labels for visualization
        plt.axis("off")

def map_labels(label):
    """
    Maps binary labels to 'real' and 'Aigen'.
    """
    if label == 1:
        return 'Real'
    else:
        return 'Ai-Gen'