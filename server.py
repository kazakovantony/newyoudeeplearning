from bottle import post, get, request, run, install, response, BaseRequest
import log_service
import json

import predictor_facade_factory

BaseRequest.MEMFILE_MAX = 1024 * 1024 * 20

@post('/prediction/movings')
def predict():
    def execute_predict(request):
        predictor = predictor_facade_factory.get_predictor_facade(request)
        return predictor.predict(request.json)
    
    return log_service.decorate_with_log(execute_predict, request, response)

@get('/prediction/logs')
def get_logs():
    response.set_header('Content-Type', 'application/json')
    return json.dumps(log_service.get_logs(request))

@get('/prediction/logs/<file_name>')
def get_log(file_name):
    response.set_header('Content-Type', 'application/json')
    return log_service.get_log(file_name)

run(host='localhost', port=5000, debug=True)