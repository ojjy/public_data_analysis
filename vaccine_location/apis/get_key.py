from pathlib import Path
import os
import json


def get_apikey(key_name, json_filename):
    BASE_DIR = Path(__file__).resolve().parent # == os.path.dirname(os.path.abspath(__file__))
    json_filepath = os.path.join(BASE_DIR, json_filename)

    if(not os.path.isfile(json_filepath)):
        print("JSON File Not Found")
        raise FileNotFoundError

    with open(json_filepath) as f:
        json_p = json.loads(f.read())
        # print("json_p:  ", json_p)

    try:
        value=json_p[key_name]
        return value
    except KeyError:
        error_msg = "ERROR: Unvalid Key"
        return error_msg
