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
Dockerfile中拉取的ubuntu20.04-py38镜像构建脚本：
```Dockerfile
ROM ubuntu:20.04
# 设置时区为你需要的时区为亚洲/上海
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
    echo "Asia/Shanghai" > /etc/timezone
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
    apt-get install -y python3.8 && \
    apt-get install -y python3-pip && \
    apt-get install -y git && \
    apt-get install -y vim
ENV PATH="/usr/bin:${PATH}"
# 设置默认 Python 版本
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 1
RUN pip3 install --upgrade pip
# 安装依赖的python库
RUN pip install pycryptodome && \
pip install fastapi==0.95.1 && \
pip install numpy==1.24.3 && \
pip install pandas==2.0.1 && \
pip install paramiko==2.7.2 && \
pip install Pillow==9.5.0 && \
pip install PyYAML==6.0.1 && \
pip install requests==2.30.0 && \
pip install scipy==1.10.1 && \
pip install six==1.16.0 && \
pip install urllib3==1.26.15 && \
pip install uvicorn==0.22.0 && \
pip install xlrd==2.0.1 && \
pip install beautifulsoup4==4.12.2 

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


