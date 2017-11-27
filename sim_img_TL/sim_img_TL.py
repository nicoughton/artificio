"""

 sim_img_TL.py  (author: Anson Wong / git: ankonzoid)

 Uses transfer learning on pre-trained VGG image classification models to
 get feature vectors and plot the tSNE of the feature vectors.

"""
import numpy as np
import sys, os
sys.path.append("src")
from vgg16 import VGG16
from vgg19 import VGG19
from keras.preprocessing import image
from keras.models import Model
from imagenet_utils import preprocess_input
from tSNE import run_tsne

def main():
    # Set model
    print()
    if 0:
        # Remove last layer, to get multiple filters
        print("Using VGG16 pre-trained model...")
        model = VGG16(weights='imagenet',
                      include_top=False)  # remove output layer
    else:
        print("Using VGG19 pre-trained model...")
        base_model = VGG19(weights='imagenet')
        model = Model(input=base_model.input,
                      output=base_model.get_layer('block4_pool').output)

    # Import images and features
    imgs_plot, X = [], []
    path = "db"
    print("Reading images from '{}'...".format(path))
    valid_image_formats = [".jpg", ".jpeg"]
    for f in os.listdir(path):
        ext = os.path.splitext(f)[1]
        if ext.lower() not in valid_image_formats:
            continue

        # Read image file
        filename = os.path.join(path,f)  # filename
        img = image.load_img(filename, target_size=(224, 224))  # load
        imgs_plot.append(np.array(img))  # append original (resized) image array

        # Pre-process for model input
        img = image.img_to_array(img)  # convert to array
        img = np.expand_dims(img, axis=0)
        img = preprocess_input(img)
        features = model.predict(img).flatten()  # features
        X.append(features)  # append feature extractor

    # Convert
    X = np.array(X)
    imgs_plot = np.array(imgs_plot)
    print(" X_features = {}".format(X.shape))
    print(" imgs_plot = {}".format(imgs_plot.shape))

    # Plot tSNE
    print("Plotting tSNE to output/tsne.png...")
    run_tsne(imgs_plot, X, "output/tsne.png")

# Driver
if __name__ == "__main__":
    main()