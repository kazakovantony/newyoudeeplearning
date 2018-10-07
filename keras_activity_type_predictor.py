class KerasActivityTypePredictor:
    def __init__(self, native_keras_model, binarizer, sample_size, features):
        self.native_keras_model = native_keras_model
        self.binarizer = binarizer
        self.sample_size = sample_size
        self.features = features
        
    def predict(self, samples):
        return self.binarizer.inverse_transform(self.native_keras_model.predict(samples))
        
    def get_sample_size(self):
        return self.sample_size
    
    def get_features(self):
        return self.features