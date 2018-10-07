import pickle
import json

def read_obj_from_file(path_to_file):
    with open(path_to_file, 'rb') as input_file:
        return pickle.load(input_file)
    
def write_obj_to_file(obj, path_to_file):
    with open(path_to_file, 'wb') as output:
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)
        
def write_json_to_file(obj, path_to_file):
    with open(path_to_file, "w", encoding="utf-8") as file:
        json.dump(obj, file)

def read_json_from_file(path_to_file):
    return json.loads(open(path_to_file, 'r').read())