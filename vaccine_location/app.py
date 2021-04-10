from flask import Flask, render_template
import pandas as pd
from sqlalchemy import create_engine
from folium import Map, Marker, Icon, Figure
from folium.plugins import MarkerCluster
import folium
import requests
import json
import os
from pathlib import Path

app = Flask(__name__)
# 애초에 주소 리스트를 생성하여 주소 찍을때 이 리스트를 넘겨 한번만 콜하여 지도에 찍는 방법이 있는지 강구.
def get_apikey(key_name, json_filename):
    # 해당 py파일의 속해 있는 폴더가 base_dir
    BASE_DIR = Path(__file__).resolve().parent # == os.path.dirname(os.path.abspath(__file__))
    # 해당 프로젝트 파일내 json파일이 있으므로 폴더패스와 파일이름을 합쳐 json_file의 절대경로값 얻는다
    json_filepath = os.path.join(BASE_DIR, json_filename)

    # json_file이 존재하지 않으면 error 발생
    if(not os.path.isfile(json_filepath)):
        print("JSON File Not Found")
        raise FileNotFoundError

    # json파일이 존재하면 json파일내의 모든 key, value값을 얻는다
    with open(json_filepath) as f:
        json_p = json.loads(f.read())
        # print("json_p:  ", json_p)

    try:
        # key에 해당하는 value를 얻는다 ex. json_p["Authorization"]
        value=json_p[key_name]
        # print(value)
        return value
    except KeyError:
        # 해당하는 key_name이 없는 경우이다
        error_msg = "ERROR: Unvalid Key"
        return error_msg

# 잘못된 주소정보를 가져와도 에러가 발생하지 않도록 try except구문을 넣어 수정필요
# if else구문으로 에러처리 할지 try except구문으로 에러 처리 할지 성능비교 필요
def getLatLng(addr):
    value = get_apikey(key_name="Authorization", json_filename="secret.json")
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


def check_error_addr():
    """
    주소에러 체크 csv 파일 내 올바른 위도경도 값을 찾을수 있도록 지도로 찍기전 getLanLat함수를 호출하여 오류 검사를 한다.
    :return:
    """
    df = pd.read_csv("csv/vac210407.csv")
    addr_list=[]
    for idx in range(len(df)):
        addr_list.append(df.loc[idx, "주소"])
    addr_lon_list, addr_lat_list = getLatLng_list(addr_list)

def getLatLng_list(addr_list):
    key_name = "Authorization"
    value = get_apikey(key_name, json_filename="secret.json")
    headers={key_name: value}
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

@app.route('/test')
def test_location():
    map = folium.Map(
        location=[36.5053542, 127.7043419]
    )
    lon, lat = getLatLng("대전광역시 유성구 유성대로 978")
    Marker(location=[lon, lat], popup="test location", icon=Icon(color='green', icon='flag')).add_to(map)
    return map._repr_html_()
@app.route('/2')
def modify_check():
    return "<h1>modified 210403</h1>"

@app.route('/1')
def base():
    map = folium.Map(
        location=[36.5053542, 127.7043419]
    )
    # 처음 csv파일을 읽을때 976으로 되어 있는데 확인해보니 카카오api에는 등록되어 있지 않는 잘못된 주소 정보로 978로 수정하니 정상적으로 위도 경도 값을 가져온다.
    addr_lon, addr_lat = getLatLng("대전광역시 유성구 유성대로 978")
    return map._repr_html_()

@app.route('/map')
def draw_map_multiple_function_call():
    # db연결
    # dbcon = create_engine("mysql+pymysql://test:test@127.0.0.1/testdb")
    # df = pd.read_csv("vac.csv")
    # df = pd.read_csv("vac210315.csv")
    df = pd.read_csv("csv/vac210407.csv")
    # dataframe내 데이터를 db에 넣는다 테이블이 없으면 생성하고 테이블과 데이터가 있으면 삭제하고 다시 생성
    # df.to_sql(name='vaccine_loc', con=dbcon, if_exists='replace')
    # # row갯수 만큼 for문을 돌아서 row들의 데이터를 각각 저장한다 iterrows()

    m = Map(location=[36.5053542, 127.7043419], zoom_start=8)

    # print(df)
    for idx in range(len(df)):
        # print(df.loc[idx, "시설명"], df.loc[idx, "주소"])
        location_name = df.loc[idx, "시설명"]
        addr = df.loc[idx, "주소"]
        addr_lon, addr_lat = getLatLng(addr)
        iframe = location_name+ ":<br> "+ addr
        popup = folium.Popup(iframe, min_width=200, max_width=200)
    # 데이터내 주소를 마커형태로 지도에 찍는다
        Marker(location=[addr_lat, addr_lon], popup=popup, tooltip=location_name, icon=Icon(color='green', icon='flag')).add_to(m)
    return m._repr_html_()

@app.route('/')
def draw_map_once_function_call():
    # db연결
    # dbcon = create_engine("mysql+pymysql://test:test@127.0.0.1/testdb")
    # df = pd.read_csv("vac.csv")
    # df = pd.read_csv("vac210315.csv")
    df = pd.read_csv("csv/vac210331.csv")
    # dataframe내 데이터를 db에 넣는다 테이블이 없으면 생성하고 테이블과 데이터가 있으면 삭제하고 다시 생성
    # df.to_sql(name='vaccine_loc', con=dbcon, if_exists='replace')
    # # row갯수 만큼 for문을 돌아서 row들의 데이터를 각각 저장한다 iterrows()


    m = Map(location=[36.5053542, 127.7043419], zoom_start=8)

    addr_list=[]
    for idx in range(len(df)):
        addr_list.append(df.loc[idx, "주소"])

    # 여러번 호출하지 않고 함수는 1번만 호출하고 값들은 리스트 형태로 반환한다
    lon_list, lat_list = getLatLng_list(addr_list)

    for idx, addr in enumerate(addr_list):
        location_name=df.loc[idx, "시설명"]
        iframe = location_name + ":<br> " + addr
        popup = folium.Popup(iframe, min_width=200, max_width=200)
        Marker(location=[lat_list[idx], lon_list[idx]], popup=popup, tooltip=location_name, icon=Icon(color='green', icon='flag')).add_to(m)
    account_info=get_apikey("Account","secret.json")
    return render_template(template_name_or_list="index.html",
                           map=m._repr_html_(),
                           account_info=account_info)


if __name__ == '__main__':
    # csv파일이 바뀌면 flask서버를 돌리기전 주소체크만 먼저 하고 주소의 오류가 없는지 먼저 검사한다.
    check_error_addr()

    #csv파일내 오류가 없으면 즉 모두 정확한 위도 경도 값 가지고 올수 있으면 flask서버 실행
    host_addr = '0.0.0.0'
    port_num = '5000'
    app.run(host=host_addr, port=port_num, debug=True)



# References
# https://www.geeksforgeeks.org/different-ways-to-iterate-over-rows-in-pandas-dataframe/
# https://www.geeksforgeeks.org/python-pandas-dataframe-loc/
# Address http://yejinjo.com

# csv파일내 주소 변경 사항
# 10,지역,코로나19 대전광역시 유성구 예방접종센터,,유성종합스포츠센터,34128,대전광역시 유성구 유성대로 976 => 978
# 63,지역,코로나19 전라남도 광양시 예방접종센터 ,,광양실내체육관,57728,전남 광양시 봉강면 매천 695-20 => 광양읍
