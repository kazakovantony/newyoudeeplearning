import pandas as pd
import numpy as np

class PredictorFacade:
    def __init__(self, activity_type_predictor, activity_type_samples_preparator, predictor_result_factory):        
        self.activity_type_predictor = activity_type_predictor
        self.activity_type_samples_preparator = activity_type_samples_preparator
        self.predictor_result_factory = predictor_result_factory
    
    def predict(self, input_df):
        input_df = input_df.sort_values(by='time').reset_index(drop=True)
        samples = self.activity_type_samples_preparator.prepare(input_df)
            
        predicted_activity_types = self.activity_type_predictor.predict(samples)
        
        return self.predictor_result_factory.create(predicted_activity_types, input_df)
    
class JsonPredictorFacadeAdapter:
    def __init__(self, predictor_facade):
        self.predictor_facade = predictor_facade
        
    def predict(self, input_data):
        return self.predictor_facade.predict(pd.DataFrame(input_data)).to_json(orient='records')
    
class SplitJsonPredictorFacadeAdapter:
    def __init__(self, predictor_facade):
        self.predictor_facade = predictor_facade
        
    def predict(self, input_data):
        return self.predictor_facade.predict(pd.DataFrame(input_data['data'], columns=input_data['columns'])).to_json(orient='records')
        