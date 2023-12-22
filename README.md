# bge-base-api
# bge-api

BGE-base Embeddings api by FastAPI,python==3.8.0
## 0.下载模型文件
- 模型文件存储路径：/home/app/model/bge-base-zh-v1.5
- 使用git clone下载模型文件：git clone https://www.modelscope.cn/Xorbits/bge-base-zh-v1.5.git
- 下载完毕后，需要安装git-lfs，代码如下：
```shell
cd /home/app/model/bge-base-zh-v1.5
sudo apt-get install git-lfs
git lfs install
git lfs pull

```

## 1.构建镜像
在Dockerfile所在路径执行下面命令创建镜像。
```shell
docker build -t bge-base-api:v1.0 .
```
## 2.启动镜像
### CPU

```sh
docker run -d -p 6008:6008  --name bge-base-api bge-base-api:v1.0
```

### GPU

> required nvidia-docker2

```sh
docker run -d -p 6008:6008 --gpus all --name bge-base-api bge-base-api:v1.0
```

## 3.测试服务

```python
import requests
import json
url = "http://localhost:6008/bge-base/post"
data = {
    "text":"你好，很高兴见到你",
}
response = requests.post(url, data=json.dumps(data),headers={'Content-Type': 'application/json'})
# 打印响应
if response.status_code == 200:
    # 获取响应内容并打印
    print("Response:", response.json())
else:
    print("Request failed with status code:", response.status_code)
```
返回结果：
```
Response: {'text': '你好，很高兴见到你', 'embedding': [-0.01212986558675766, -0.009481322951614857, -0.0041494425386190414, ..., 0.011346199549734592, -0.0002315840683877468, -0.055745672434568405], 'request_time': '2023-12-22 18:07:44', 'response_time': '2023-12-22 18:07:44', 'code': 200}

```


