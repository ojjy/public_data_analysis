import requests
import json
url = "https://api.odcloud.kr/api/15077586/v1/centers?page=1&perPage=300&serviceKey="

headers = {"Authorization":""}

result = requests.get(url=url, headers=headers)
json_result = json.loads(str(result.text))
print(json_result)

with open("result.json", "w", encoding='utf-8') as fp:
    json.dump(json_result, fp, ensure_ascii=False)
