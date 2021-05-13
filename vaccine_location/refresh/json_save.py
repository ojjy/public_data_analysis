from flask import Flask, render_template
import requests
import json
import folium
from folium import Map, Marker, Icon
from folium.plugins import MarkerCluster
# app = Flask(__name__)
# serviceKey="pC39hvcQg6mW%2Bozlig8RxFoR40NkT%2FymzBYy8P9Sze7qQdWhzWISUXn2hIGSEB9d1XAOYy1IDb2U0VmkeVyRuQ%3D%3D"
# url = "https://api.odcloud.kr/api/15077586/v1/centers?page=1&perPage=300&serviceKey="+serviceKey
#
# result = requests.get(url=url)
# json_result = json.loads(str(result.text))
#
# for idx in range(json_result["currentCount"]):
#     print(json_result["data"][idx]["address"])
#
# with open("result.json", "w", encoding='utf-8') as fp:
#     json.dump(json_result, fp, ensure_ascii=False)

# @app.route("/")
def map_api_call():
    serviceKey = "pC39hvcQg6mW%2Bozlig8RxFoR40NkT%2FymzBYy8P9Sze7qQdWhzWISUXn2hIGSEB9d1XAOYy1IDb2U0VmkeVyRuQ%3D%3D"
    url = "https://api.odcloud.kr/api/15077586/v1/centers?page=1&perPage=300&serviceKey=" + serviceKey

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
        print(iframe)
        # popup = folium.Popup(iframe, min_width=200, max_width=200)
        # Marker(location=[lat, lng], popup=popup, tooltip=centerName+" : "+facilityName, icon=Icon(color='green', icon='flag')).add_to(marker_cluster)
        # return render_template(template_name_or_list="index.html",  map=m._repr_html_())


if __name__ == "__main__":
    map_api_call()