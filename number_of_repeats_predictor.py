import pandas as pd
import numpy as np

class NumberOfRepeatsPredictor:    
    def _process_fft_result(self, fft_result):
        magnitudes = np.abs(fft_result);
        magnitudes = np.sum(magnitudes, 1);
        magnitudes = magnitudes * 2 / magnitudes.shape[0];
        magnitudes = np.array_split(magnitudes,2)[0];
        magnitudes = magnitudes[1:];
        return magnitudes;

    def predict(self, df):
        input = df[['y_axis', 'z_axis', 'ay_axis']]
        fft_result = np.fft.fftn(input, s=None, axes=None, norm=None);
        magnitudes = self._process_fft_result(fft_result);
        max = magnitudes.max();
        threshold = max / 1.45;
        top_frequencies = np.argwhere(magnitudes > threshold);
        predicted = top_frequencies.min();
        return predicted
