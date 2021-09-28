import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array



class Model:
    def __init__(self, ):
        self.model = load_model('saved_model/mobilenet.hdf5')

    def get_img(self, path):
        img = img_to_array(load_img(path, target_size=(150,150,3)))
        img = np.expand_dims(img, axis=0)

        return img
        
    def predict(self, imgpath):
        img = self.get_img(imgpath)
        prediction = self.model.predict(img)[0][0]

        return prediction

