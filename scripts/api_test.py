import requests
import json
url = "http://localhost:6008/bge-base/post"
# url = "http://192.168.31.252:6008/bge-base/post"
data = {
    "text":"你好，很高兴见到你",
}
response = requests.post(url, data=json.dumps(data),headers={'Content-Type': 'application/json'})
# 打印响应
if response.status_code == 200:
    # 获取响应内容并打印
    response_data = response.json()
    print("Response:", response_data)
else:
    print("Request failed with status code:", response.status_code)
