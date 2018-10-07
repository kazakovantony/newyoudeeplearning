import pandas as pd
import numpy as np
import datetime

MIN_COUNT_OF_SAME_IN_LINE = 2

class PredictorResultFactory:    
    def __init__(self, sample_size, number_of_repeats_predictor):        
        self.sample_size = sample_size
        self.number_of_repeats_predictor = number_of_repeats_predictor
    
    def _calculate_duration(self, activity_df):        
        time_s = activity_df['time']
        duration_in_seconds = (time_s.iloc[-1] - time_s.iloc[0]) // 1000
        return str(datetime.timedelta(seconds=int(duration_in_seconds)))
    
    def _find_activity_df(self, prediction_index, count_of_same_in_line, input_df):
        sample_start = (prediction_index - count_of_same_in_line + 1) * self.sample_size
        sample_end = prediction_index * self.sample_size
        
        return input_df[sample_start:sample_end].sort_values(by='time').reset_index(drop=True)
    
    def _determine_number_repeats(self, activity_df, predicted_activity_type):
        if predicted_activity_type == 'pause':
            return 1
        
        return self.number_of_repeats_predictor.predict(activity_df)
    
    def _create(self, predicted_activity_type, prediction_index, count_of_same_in_line, input_df):
        activity_df = self._find_activity_df(prediction_index, count_of_same_in_line, input_df)
        
        return [predicted_activity_type, self._calculate_duration(activity_df), self._determine_number_repeats(activity_df, predicted_activity_type)]
    
    def create(self, predicted_activity_types, input_df):
        predictor_results = []
        
        count_of_same_in_line = 0
        previes_prediction = predicted_activity_types[0]
        
        for prediction_index in range(len(predicted_activity_types)):
            prediction = predicted_activity_types[prediction_index]
            
            if prediction == previes_prediction:
                count_of_same_in_line = count_of_same_in_line + 1
            else:
                if count_of_same_in_line >= MIN_COUNT_OF_SAME_IN_LINE:
                    predictor_results.append(self._create(previes_prediction, prediction_index, count_of_same_in_line, input_df))
                previes_prediction = prediction
                count_of_same_in_line = 1
        
        if count_of_same_in_line >= MIN_COUNT_OF_SAME_IN_LINE:
            predictor_results.append(self._create(previes_prediction, len(predicted_activity_types) - 1, count_of_same_in_line, input_df))
                
        return pd.DataFrame(predictor_results, columns=['activity', 'duration', 'number_of_repeats'])