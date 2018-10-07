import keras
import common_io
from keras_activity_type_predictor import KerasActivityTypePredictor

KERAS_SAMPLE_SIZE = 100
KERAS_PATH_TO_MODEL = 'model_config/model.hdf5'
KERAS_PATH_TO_BINARIZER = 'model_config/binarizer.pkl'
KERAS_MODEL_FEATURES = ['ax_axis', 'ay_axis', 'az_axis', 'magn_z', 'x_axis', 'y_axis', 'z_axis']

keras_predictor = None   

def get():        
    def create_keras_activity_type_predictor():
        native_keras_model = keras.models.load_model(KERAS_PATH_TO_MODEL)
        binarizer = common_io.read_obj_from_file(KERAS_PATH_TO_BINARIZER)
        
        return KerasActivityTypePredictor(native_keras_model, binarizer, KERAS_SAMPLE_SIZE, KERAS_MODEL_FEATURES)
    
    global keras_predictor
    if keras_predictor is None:
        keras_predictor = create_keras_activity_type_predictor()
        
    return keras_predictor