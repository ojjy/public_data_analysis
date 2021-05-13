from flask import Flask, render_template
import requests
import json
import folium
from folium import Map, Marker, Icon
from folium.plugins import MarkerCluster
from apis.get_key import get_apikey

app = Flask(__name__)
serviceKey=get_apikey("serviceKey", "secret.json")
url = "https://api.odcloud.kr/api/15077586/v1/centers?page=1&perPage=300&serviceKey="+serviceKey

result = requests.get(url=url)
json_result = json.loads(str(result.text))

for idx in range(json_result["currentCount"]):
    print(json_result["data"][idx]["address"])

#
# with open("result.json", "w", encoding='utf-8') as fp:
#     json.dump(json_result, fp, ensure_ascii=False)

@app.route("/")
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
    return render_template(template_name_or_list="index.html",  map=m._repr_html_(), account_info=account_info)


if __name__ == '__main__':
    host_addr = '0.0.0.0'
    port_num = '5000'
    app.run(host=host_addr, port=port_num, debug=True)