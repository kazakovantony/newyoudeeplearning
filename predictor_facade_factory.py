from predictor_facade import PredictorFacade
from predictor_facade import JsonPredictorFacadeAdapter
from predictor_facade import SplitJsonPredictorFacadeAdapter
from activity_type_sampes_preparator import ActivityTypeSampelsPreparator
from predictor_result_factory import PredictorResultFactory
import keras_activity_type_predictor_factory
from number_of_repeats_predictor import NumberOfRepeatsPredictor

def _create_predictor_facade():
    activity_type_predictor = keras_activity_type_predictor_factory.get()
    activity_type_samples_preparator = ActivityTypeSampelsPreparator(activity_type_predictor)
    predictor_result_factory = PredictorResultFactory(activity_type_predictor.get_sample_size(), NumberOfRepeatsPredictor())
        
    return PredictorFacade(activity_type_predictor, activity_type_samples_preparator, predictor_result_factory)

json_predictor_facade = None
def _get_json_predictor_facade():
    global json_predictor_facade
    if json_predictor_facade is None:
        json_predictor_facade = JsonPredictorFacadeAdapter(_create_predictor_facade())
    
    return json_predictor_facade

split_json_predictor_facade = None
def _get_split_json_predictor_facade():
    global split_json_predictor_facade
    if split_json_predictor_facade is None:
        split_json_predictor_facade = SplitJsonPredictorFacadeAdapter(_create_predictor_facade())
    
    return split_json_predictor_facade

def get_predictor_facade(request):
    if isinstance(request.json, list):
        return _get_json_predictor_facade()
    
    return _get_split_json_predictor_facade()
    
    
