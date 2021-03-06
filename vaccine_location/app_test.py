import requests
import json
import os
from pathlib import Path
import pandas as pd


# github등 git서버에 올릴때 개인적으로 받은 api key등을 올리지 않도록 gitignore에 secret.json을 등록하고 이 키값은 json파일에 등록
def get_apikey(key_name, json_filename='secret.json'):
    print("get_apikey call")
    # 해당 py파일의 속해 있는 폴더가 base_dir
    BASE_DIR = Path(__file__).resolve().parent # == os.path.dirname(os.path.abspath(__file__))
    # 해당 프로젝트 파일내 json파일이 있으므로 폴더패스와 파일이름을 합쳐 json_file의 절대경로값 얻는다
    json_filepath = os.path.join(BASE_DIR, json_filename)

    # json_file이 존재하지 않으면 error 발생
    if(not os.path.isfile(json_filepath)):
        raise FileNotFoundError

    # json파일이 존재하면 json파일내의 모든 key, value값을 얻는다
    with open(json_filepath) as f:
        json_p = json.loads(f.read())
        print("json_p:  ", json_p)

    try:
        # key에 해당하는 value를 얻는다 ex. json_p["Authorization"]
        value=json_p[key_name]
        print(value)
        return value
    except KeyError:
        # 해당하는 key_name이 없는 경우이다
        error_msg = "ERROR: Unvalid Key"
        return error_msg

# 잘못된 주소정보를 가져와도 에러가 발생하지 않도록 try except구문을 넣어 수정필요
def getLatLng(addr):

    Authorization = get_apikey("Authorization")
    url = 'https://dapi.kakao.com/v2/local/search/address.json?query=' + addr
    headers = {"Authorization": Authorization}
    result = json.loads(str(requests.get(url, headers=headers).text))
    status_code = requests.get(url, headers=headers).status_code
    if(status_code != 200):
        print(f"ERROR: Unable to call rest api, http_status_coe: {status_code}")
        return 0
    print(requests.get(url, headers=headers))
    print(result)

    try:
        match_first = result['documents'][0]['address']
        lon = match_first['x']
        lat = match_first['y']
        print(lon, lat)
        print(match_first)

        return lon, lat
    except IndexError: # match값이 없을때
        return 0
    except TypeError: # match값이 2개이상일때
        return 0

def enumerate_test():
    df = pd.read_csv("csv/vac.csv")

    addr_list=[]

    for df_idx in range(len(df)):
        addr = df.loc[df_idx, "주소"]
        addr_list.append(addr)

    for idx, addr in enumerate(addr_list):
        print(idx,"번째 주소: " ,addr)

    # result = json.loads(str(requests.get(url, headers=headers).text))
def get_test(addr):
    # 왜 {key_name, value}를 프린트하면 {value, key_name} 일까?
    key_name = "Authorization"
    value = get_apikey(key_name)
    headers = {key_name: value}
    print(headers)
    url = 'https://dapi.kakao.com/v2/local/search/address.json?query=' + addr
    result = requests.get(url, headers=headers)
    # content binary형태, json json형태, raw raw형태
    print("content: ", json.loads(requests.get(url=url, headers=headers).text))

    print(result)

    # return result

if __name__ == "__main__":
    # print(getLatLng("경기도 수원시 영통구 광교로 114"))


    #enumerate함수는 리스트 값을 인자로 넣어주면 인덱스와 인덱스에 해당하는 배열 데이터를 리턴해준다.
    # enumerate_test()


    get_test("전남 광양시 봉강면 매천로 695-20")
