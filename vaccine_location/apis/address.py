import json
import requests
from apis.get_key import get_apikey


def getlatlng_list_naver(addr_list):
    lon_list=[]
    lat_list=[]
    key_id = get_apikey('X-NCP-APIGW-API-KEY-ID', json_filename="secret.json")
    key = get_apikey('X-NCP-APIGW-API-KEY', json_filename="secret.json")
    headers = {'X-NCP-APIGW-API-KEY-ID':key_id,
               'X-NCP-APIGW-API-KEY':key}
    for idx, addr in enumerate(addr_list):
        url = 'https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode?query='+addr
        result = json.loads(str(requests.get(url=url, headers=headers).text))
        try:
            addr_info_lon = result['addresses'][0]['x']
            addr_info_lat = result['addresses'][0]['y']
            lon_list.append(addr_info_lon)
            lat_list.append(addr_info_lat)
        except IndexError:  # match값이 없을때
            print("IndexError발생, 해당 주소에 맞는 위도 경도 없음, idx: ",idx, "번째, 주소정보: ", addr)
            raise IndexError
        except TypeError:  # match값이 2개이상일때
            print("TypeError발생, 해당 주소에 맞는 위도 경도값 2개 이상, idx: ",idx, "번째, 주소정보: ", addr)
            raise TypeError
    return lon_list, lat_list

def getlatlng_naver(addr):
    key_id = get_apikey('X-NCP-APIGW-API-KEY-ID', json_filename="secret.json")
    key = get_apikey('X-NCP-APIGW-API-KEY', json_filename="secret.json")
    headers = {'X-NCP-APIGW-API-KEY-ID':key_id,
               'X-NCP-APIGW-API-KEY':key}
    url = 'https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode?query='+addr
    result = json.loads(str(requests.get(url=url, headers=headers).text))
    try:
        addr_info_lon = result['addresses'][0]['x']
        addr_info_lat = result['addresses'][0]['y']
    except IndexError:  # match값이 없을때
        print("IndexError발생, 해당 주소에 맞는 위도 경도 없음, 주소정보: ", addr)
        raise IndexError
    except TypeError:  # match값이 2개이상일때
        print("TypeError발생, 해당 주소에 맞는 위도 경도값 2개 이상, 주소정보: ", addr)
        raise TypeError
    return addr_info_lon, addr_info_lat

def getLatLng(addr):
    value = get_apikey(key_name="KAKAO_Authorization", json_filename="secret.json")
    headers = {"Authorization": value}
    url = 'https://dapi.kakao.com/v2/local/search/address.json?query=' + addr
    result = json.loads(str(requests.get(url, headers=headers).text))
    status_code = requests.get(url, headers=headers).status_code
    if(status_code != 200):
        print(f"ERROR: Unable to call rest api, http_status_coe: {status_code}")
        return 0
    # print(requests.get(url, headers=headers))
    # print(result)

    try:
        match_first = result['documents'][0]['address']
        lon = match_first['x']
        lat = match_first['y']
        # print(lon, lat)
        # print(match_first)

        return lon, lat
    except IndexError: # match값이 없을때
        print("IndexError발생, 해당 주소에 맞는 위도 경도 없음, 주소정보: ", addr)
        raise IndexError
    except TypeError: # match값이 2개이상일때
        print("TypeError발생, 해당 주소에 맞는 위도 경도값 2개 이상, 주소정보: ", addr)
        raise TypeError


def getLatLng_list(addr_list):
    key_name = "KAKAO_Authorization"
    value = get_apikey(key_name, json_filename="secret.json")
    headers={"Authorization": value}
    lon_list=[]
    lat_list=[]
    for idx, addr in enumerate(addr_list):
        url = 'https://dapi.kakao.com/v2/local/search/address.json?query=' + addr
        result = requests.get(url=url, headers=headers)
        if(result.status_code != 200):
            raise ValueError

        # json으로 로드 하지 않으면 dict형식으로 불러올수 없다
        addr_info = json.loads(result.text)
        try:
            addr_info_lon = addr_info["documents"][0]['address']['x']
            addr_info_lat = addr_info["documents"][0]['address']['y']
            lon_list.append(addr_info_lon)
            lat_list.append(addr_info_lat)

        except IndexError:  # match값이 없을때
            print("IndexError발생, 해당 주소에 맞는 위도 경도 없음, idx: ",idx, "번째, 주소정보: ", addr)
            raise IndexError
        except TypeError:  # match값이 2개이상일때
            print("TypeError발생, 해당 주소에 맞는 위도 경도값 2개 이상, idx: ",idx, "번째, 주소정보: ", addr)
            raise TypeError

    return lon_list, lat_list

if __name__ == "__main__":
    print(getlatlng_naver(["경기도 수원시 영통구 광교로 114"]))