from apis.get_key import get_apikey
import requests
import json
import math

def vaccine_location():

    url = f"https://api.odcloud.kr/api/15077756/v1/vaccine-stat?page=1&perPage=10&serviceKey={get_apikey('serviceKey', 'secret.json')}"
    json_data = json.loads(requests.get(url=url).text)
    # print(json_data)
    maxpageno = math.ceil(json_data["totalCount"]/json_data["perPage"])
    # print(maxpageno)
    for pageno in range(1, maxpageno+1):
        url = f"https://api.odcloud.kr/api/15077756/v1/vaccine-stat?page={pageno}&perPage={json_data['perPage']}&serviceKey={get_apikey('serviceKey', 'secret.json')}"
        json_data = json.loads(requests.get(url).text)
        items = json_data["data"]
        print(items[0])
        # for idx, item in enumerate(items):
        #     for key_value in item.items():
        #         print(f"key_value: {key_value}")

if __name__ == "__main__":
    vaccine_location()