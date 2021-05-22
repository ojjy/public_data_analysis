from apis.get_key import get_apikey
import requests
import json
import math

def vaccine_location():
    url = f"https://api.odcloud.kr/api/15077586/v1/centers?page=1&perPage=263&returnType=json&serviceKey={get_apikey('serviceKey', 'secret.json')}"
    json_data = json.loads(requests.get(url=url).text)
    print(json_data)
    maxpageno = math.ceil(json_data["totalCount"]/json_data["perPage"])
    print(maxpageno)
    for pageno in range(1, maxpageno+1):
        url = f"https://api.odcloud.kr/api/15077586/v1/centers?page={pageno}&perPage={json_data['perPage']}&serviceKey={get_apikey('serviceKey', 'secret.json')}"
        json_data = json.loads(requests.get(url).text)
        items = json_data["data"]
        for idx, item in enumerate(items):
            print(idx, item)

if __name__ == "__main__":
    vaccine_location()