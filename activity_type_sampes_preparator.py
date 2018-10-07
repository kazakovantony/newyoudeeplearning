import pandas as pd
import numpy as np

class ActivityTypeSampelsPreparator:
    def __init__(self, activity_type_predictor):        
        self.activity_type_predictor = activity_type_predictor
        
    def prepare(self, df):
        sample_size = self.activity_type_predictor.get_sample_size()
        number_of_samples = df.shape[0] // sample_size
        features = self.activity_type_predictor.get_features()
        
        df = df[features]
        df = df[0: (number_of_samples * sample_size)]
        return df.values.reshape((number_of_samples, sample_size, df.shape[1]))