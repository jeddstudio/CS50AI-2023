import cv2
import numpy as np
import os
import sys
import tensorflow as tf

from sklearn.model_selection import train_test_split

EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python traffic.py data_directory [model.h5]")

    # Get image arrays and labels for all image files
    images, labels = load_data(sys.argv[1])

    # Split data into training and testing sets
    labels = tf.keras.utils.to_categorical(labels)
    x_train, x_test, y_train, y_test = train_test_split(
        np.array(images), np.array(labels), test_size=TEST_SIZE
    )

    # Get a compiled neural network
    model = get_model()

    # Fit model on training data
    model.fit(x_train, y_train, epochs=EPOCHS)

    # Evaluate neural network performance
    model.evaluate(x_test,  y_test, verbose=2)

    # Save model to file
    if len(sys.argv) == 3:
        filename = sys.argv[2]
        model.save(filename)
        print(f"Model saved to {filename}.")


def load_data(data_dir):
    """
    Load image data from directory `data_dir`.

    Assume `data_dir` has one directory named after each category, numbered
    0 through NUM_CATEGORIES - 1. Inside each category directory will be some
    number of image files.

    Return tuple `(images, labels)`. `images` should be a list of all
    of the images in the data directory, where each image is formatted as a
    numpy ndarray with dimensions IMG_WIDTH x IMG_HEIGHT x 3. `labels` should
    be a list of integer labels, representing the categories for each of the
    corresponding `images`.
    """
    images = []
    labels = []
    not_processed_image = []

    for category in range(NUM_CATEGORIES): # it is a folder number
        # Document given `os.path.join()`, auto use "/" or "\", no matter user is using macOS, Linux, Windows, platform-independent
        category_path = os.path.join(data_dir, str(category)) # gtsrb0/0, gtsrb/25
        
        # Loop through all images in the folder(category_path)
        for image_name in os.listdir(category_path): # `image_name` e.g. "00023_00012.ppm"
            
            image_path = os.path.join(category_path, image_name) # gtsrb/38/00023_00012.ppm
            
            ### `cv2` function to turn a image to list of list
            image = cv2.imread(image_path) # It will be list of list, use the ### Image tester ### to check how it look like

            # `cv2` function to resize image
            resized_image = cv2.resize(image, (IMG_WIDTH, IMG_HEIGHT))

            if resized_image.shape == (30, 30, 3):
                # Add the processed image to the images list
                images.append(resized_image)
                # `category` aka is the folder name e.g. 0, 1, 2, ...
                labels.append(category)
            else:
                not_processed_image.append(image_path)

    if len(not_processed_image) > 0:
        print("There have some image can't processe")
        print(not_processed_image)

    return (images, labels)    
    # This process will make the `resized_image` and `labels` consistent with their index in their list 




def get_model():
    """
    ❗️❗️ We can reuse the code from the lecture source code(handwriting.py) ❗️❗️
        # And edit some parameters to fit this project

    Returns a compiled convolutional neural network model. Assume that the
    `input_shape` of the first layer is `(IMG_WIDTH, IMG_HEIGHT, 3)`.
    The output layer should have `NUM_CATEGORIES` units, one for each category.
    """
    model = tf.keras.models.Sequential([
        
        
        ############ First Convolution and Pooling ############
        # Convolutional layer
        tf.keras.layers.Conv2D(
            32, (3, 3), activation='relu', input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)
        ),
        # `32`, 32different filters
        # `(3, 3)`we are using a 3x3 filter
        # `activation='relu'` This is the activation function, ReLU (Rectified Linear Unit).
        # `input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)` The width and height use the project setup, 
            # `3` There are three colour channels (red, green and blue), so the third dimension is 3

        # Pooling Layer
        tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
        # minimize to 2x2 pixel
         # Reducing the spatial size of the feature map reduces the amount of computation and helps prevent over-simulation


        # ############ Second Convolution and Pooling ############
        # # Another convolutional layer
        # tf.keras.layers.Conv2D(
        #     64, (3, 3), activation='relu'
        # ),
        # # `64`, 64different filters
        # # `(3, 3)`we are using a 3x3 filter
        # # `activation='relu'` This is the activation function, ReLU (Rectified Linear Unit).

        # # Another Pooling Layer 
        # tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
        # # minimize to 2x2 pixel
        #  # Reducing the spatial size of the feature map reduces the amount of computation and helps prevent over-simulation


        # Flatten units
        tf.keras.layers.Flatten(), # Necessary Steps
            

        # Add a hidden layer with dropout
        tf.keras.layers.Dense(128, activation='relu'), # `128`: This means there are 128 neurons in the layer
        tf.keras.layers.Dropout(0.5), # `0.5`: This is the dropout rate, each neuron has a 50% chance of not being activated in each training iteration.


        # Output layer
        # Add an output layer with output units for all 10 digits
        tf.keras.layers.Dense(NUM_CATEGORIES, activation='softmax')
    ])

    # Compile the model
    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    return model



if __name__ == "__main__":
    main()








# ### Image tester ###
# cwd = os.getcwd()
# data_cwd = os.path.join(cwd, "gtsrb")

# category = "0"
# test_image = "00000_00011.ppm"
# test_image_path = (os.path.join(data_cwd, category, test_image))
# print("#"*15)
# print(test_image_path)
# print("#"*15)
# image = cv2.imread(test_image_path)
# # print(image)
# resized_image = cv2.resize(image, (IMG_WIDTH, IMG_HEIGHT))
# if resized_image.shape == (30, 30, 3):
#     print(resized_image.shape)