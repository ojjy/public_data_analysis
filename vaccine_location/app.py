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
def get_apikey(key_name, json_filename='secret.json'):
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
def getLatLng(addr):

    Authorization = get_apikey("Authorization")
    url = 'https://dapi.kakao.com/v2/local/search/address.json?query=' + addr
    headers = {"Authorization": Authorization}
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
        return 0
    except TypeError: # match값이 2개이상일때
        return 0

@app.route('/test')
def test_location():
    map = folium.Map(
        location=[36.5053542, 127.7043419]
    )
    lon, lat = getLatLng("대전광역시 유성구 유성대로 978")
    Marker(location=[lon, lat], popup="test location", icon=Icon(color='green', icon='flag')).add_to(map)
    return map._repr_html_()

@app.route('/index')
def base():
    map = folium.Map(
        location=[36.5053542, 127.7043419]
    )
    # 처음 csv파일을 읽을때 976으로 되어 있는데 확인해보니 카카오api에는 등록되어 있지 않는 잘못된 주소 정보로 978로 수정하니 정상적으로 위도 경도 값을 가져온다.
    addr_lon, addr_lat = getLatLng("대전광역시 유성구 유성대로 978")
    return map._repr_html_()

@app.route('/')
def hello_world():
    # db연결
    # dbcon = create_engine("mysql+pymysql://test:test@127.0.0.1/testdb")
    # df = pd.read_csv("vac.csv")
    # df = pd.read_csv("vac210315.csv")
    df = pd.read_csv("vac210331.csv")
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

if __name__ == '__main__':
    print(folium.__version__)
    host_addr = '0.0.0.0'
    port_num = '5000'
    app.run(host=host_addr, port=port_num, debug=True)


# References
# https://www.geeksforgeeks.org/different-ways-to-iterate-over-rows-in-pandas-dataframe/