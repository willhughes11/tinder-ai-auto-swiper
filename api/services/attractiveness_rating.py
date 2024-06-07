import numpy as np
from services.utility_functions import preprocess_image
from tensorflow.keras.models import load_model

class Attractiveness_Rating():
    def __init__(self):
        self.model_name = 'attractiveNet_mnv2'
        self.model_path = 'models/' + self.model_name + '.h5'
        self.model = load_model(self.model_path)


    def attractiveness_rating(self, images):
        scores = []
        for image in images:
            score = self.model.predict(np.expand_dims(preprocess_image(image,(350,350)), axis=0))
            scores.append(score[0][0])
        
        return scores


