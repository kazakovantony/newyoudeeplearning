import datetime
import uuid
import traceback
from os import listdir
import json

LOG_DIR = 'D:/android/newyouShadow/predictor/logs'

def _log(request, response, result, has_error):
    def create_base_log_file_name():
        time = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        uniq_id = uuid.uuid4()
        
        return LOG_DIR + 'time__' + time + '__id__' + str(uniq_id)
    
    def create_log_request():
        result = dict()
        
        result['remoteAddress'] = request.remote_addr
        result['method'] = request.method
        result['url'] = request.url
        result['body'] = request.body.read().decode("utf-8")
        
        return result
    
    def create_log_response(response_result, has_error):
        result = dict()
        result['hasError'] = str(has_error)
        result['body'] = str(response_result)
        
        return result
    
    def write_to_file(file_name, log):
        with open(file_name, 'w') as out:
            json.dump(log, out)
            
    base_file_name = create_base_log_file_name()
    write_to_file(base_file_name + '_request.json', create_log_request())
    write_to_file(base_file_name + '_response.json', create_log_response(result, has_error))
    response.set_header('logBaseName', base_file_name)

def decorate_with_log(function_to_wrapp, request, response):
    has_error = False
    try:
        result = function_to_wrapp(request)
    except:
        has_error = True
        result = traceback.format_exc()
        raise
    finally:
        _log(request, response, result, has_error)
        
    return result

def get_logs(request):
    print(request.url)
    url_parts = request.url.split('/')
    host = url_parts[0] + '//' + url_parts[2]
    return sorted([host + request.urlparts.path + '/' + file for file in  listdir(LOG_DIR)], reverse=True)

def get_log(file_name):
    def read_file(file_name):
        with open(file_name, 'r') as file:
            return file.read()
    
    return read_file(LOG_DIR + file_name)