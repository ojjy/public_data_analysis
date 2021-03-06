from flask import Flask, render_template
import pandas as pd
from sqlalchemy import create_engine
from folium import Map, Marker, Icon
import folium
from apis.get_key import get_apikey
from apis.address import getLatLng
from folium.plugins import MarkerCluster
import json
import requests

app = Flask(__name__)
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
    addr_lon, addr_lat = getLatLng("대전광역시 유성구 유성대로 978")
    return map._repr_html_()

# cluster기능 추가
@app.route('/map')
def draw_map_multiple_function_call():
    # db연결
    dbcon = create_engine("mysql+pymysql://test:test@127.0.0.1/testdb")
    # df = pd.read_csv("vac.csv")
    # df = pd.read_csv("vac210315.csv")
    df = pd.read_csv("csv/vac210407.csv")
    # dataframe내 데이터를 db에 넣는다 테이블이 없으면 생성하고 테이블과 데이터가 있으면 삭제하고 다시 생성
    df.to_sql(name='vaccine_center', con=dbcon, if_exists='replace')
    # # row갯수 만큼 for문을 돌아서 row들의 데이터를 각각 저장한다 iterrows()

    m = Map(location=[36.5053542, 127.7043419], zoom_start=8)

    # print(df)
    for idx in range(len(df)):
        location_name = df.loc[idx, "location_name"]
        addr = df.loc[idx, "address"]
        addr_lon, addr_lat = getLatLng(addr)
        iframe = location_name+ ":<br> "+ addr
        popup = folium.Popup(iframe, min_width=200, max_width=200)
        Marker(location=[addr_lat, addr_lon], popup=popup, tooltip=location_name, icon=Icon(color='green', icon='flag')).add_to(m)
    return m._repr_html_()


@app.route('/')
def draw_map_once_function_call():
    # df = pd.read_csv("vac.csv")
    # df = pd.read_csv("vac210315.csv")
    # df = pd.read_csv("csv/vac210331.csv")
    df = pd.read_csv("csv/test.csv")

    m = Map(location=[36.5053542, 127.7043419], zoom_start=8)
    marker_cluster = MarkerCluster().add_to(m)
    addr_list=[]
    for idx in range(len(df)):
        addr_list.append(df.loc[idx, "address"])

    # but one call func not multiple call
    # lon_list, lat_list = getLatLng_list(addr_list)

    for idx, addr in enumerate(addr_list):
        location_name=df.loc[idx, "location_name"]
        telephone = df.loc[idx, "telephone"]
        print(telephone)
        latitude = df.loc[idx, "latitude"]
        longitude = df.loc[idx, "longitude"]
        iframe = location_name + ":<br> " + addr + ": <br> " + telephone
        print(idx, ": ", iframe)
        popup = folium.Popup(iframe, min_width=200, max_width=200)
        Marker(location=[latitude, longitude], popup=popup, tooltip=location_name, icon=Icon(color='green', icon='flag')).add_to(marker_cluster)
    account_info=get_apikey("Account","secret.json")
    return render_template(template_name_or_list="index.html",
                           map=m._repr_html_(),
                           account_info=account_info)

# csv파일이 아닌 api호출을 통해 정보 get
@app.route("/reqs")
def map_api_call():
    url = "https://api.odcloud.kr/api/15077586/v1/centers?page=1&perPage=300&serviceKey=" + get_apikey("serviceKey", "secret.json")

    result = requests.get(url=url)
    json_result = json.loads(str(result.text))

    m = Map(location=[36.5053542, 127.7043419], zoom_start=8)
    marker_cluster = MarkerCluster().add_to(m)

    for idx in range(json_result["currentCount"]):
        address = json_result["data"][idx]["address"]
        centerName = json_result["data"][idx]["centerName"]
        facilityName = json_result["data"][idx]["facilityName"]
        lat = json_result["data"][idx]["lat"]
        lng = json_result["data"][idx]["lng"]
        iframe = centerName + ": <br> " + facilityName + ":<br> " + address
        popup = folium.Popup(iframe, min_width=200, max_width=200)
        Marker(location=[lat, lng], popup=popup, tooltip=centerName+" : "+facilityName, icon=Icon(color='green', icon='flag')).add_to(marker_cluster)
    account_info=get_apikey("Account","secret.json")
    return render_template(template_name_or_list="reqs.html",  map=m._repr_html_(), account_info=account_info)

if __name__ == '__main__':
    host_addr = '0.0.0.0'
    port_num = '5000'
    app.run(host=host_addr, port=port_num, debug=True)


# References
# https://www.geeksforgeeks.org/different-ways-to-iterate-over-rows-in-pandas-dataframe/
# https://www.geeksforgeeks.org/python-pandas-dataframe-loc/
# https://gist.github.com/madan712/f27ac3b703a541abbcd63871a4a56636

# Address http://yejinjo.com

# csv파일내 주소 변경 사항
# 10,지역,코로나19 대전광역시 유성구 예방접종센터,,유성종합스포츠센터,34128,대전광역시 유성구 유성대로 976 => 978
# 63,지역,코로나19 전라남도 광양시 예방접종센터 ,,광양실내체육관,57728,전남 광양시 봉강면 매천 695-20 => 광양읍
# 136,지역,코로나19 충청남도 당진시 예방접종센터,,송악문화스포츠센터,31732,충청남도 당진시 송악읍 틀모시로 830,041-360-6120
