from fastapi import FastAPI,Request
from fastapi.responses import JSONResponse
from sentence_transformers import SentenceTransformer
import uvicorn
import numpy as np
from datetime import datetime
from typing import List,Dict
import torch
import os,json,logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

class MyAPI:
    def __init__(self,):
        self.app = FastAPI()
        self.model_path = "/home/app/model/bge-base-zh-v1.5"
        print(f"开始执行模型加载")
        self.model = self.load_model()
        print("模型加载成功")

    def get_current_time(self,):
        '''
        功能：获取当前时间，时间格式：yyyy-mm-dd hh:mm:ss
        '''
        # 获取当前时间
        current_time = datetime.now()
        # 格式化为 "yyyy-mm-dd hh:mm:ss" 格式
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
        return formatted_time

    # 加载模型
    def load_model(self,):
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(
            f"本次加载模型的设备为：{'GPU: ' + torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU.'}"
        )
        return SentenceTransformer(self.model_path, device=device)

    def get_embedding(self,text:str):
        '''
        功能：对单个句子进行embedding
        '''
        # 计算嵌入向量
        embedding = self.model.encode(text, normalize_embeddings=True)
        # Min-Max normalization
        embedding = embedding / np.linalg.norm(embedding)
        embedding = embedding.tolist()
        return embedding

    def start(self):
        @self.app.post('/bge-base/post')
        # url = "http://192.168.31.232:6008/bge-base/post"
        async def handle_post_request(request: Request):
            data = await request.body()
            request_time = self.get_current_time()
            logger.info(f"接受到数据：\n{json.loads(data.decode('utf-8'))}")
            try:
                data = json.loads(data.decode('utf-8'))
                text = data["text"]
                embedding = self.get_embedding(text=text)
                response_time = self.get_current_time()
                code = 200
                response_data = {
                                     "text": text,
                                     "embedding": embedding,
                                     "request_time":request_time,
                                     "response_time":response_time,
                                     "code": code
                                     }
                return JSONResponse(content=response_data)

            except Exception as e:
                logger.info(f"{data}embedding失败！原因：\n{e}")
                code = -1
                data = json.loads(data.decode('utf-8'))
                text = data["text"]
                embedding = []
                response_time = self.get_current_time()
                response_data = {
                                      "text": text,
                                     "embedding": embedding,
                                     "request_time":request_time,
                                     "response_time":response_time,
                                     "code":code
                }
                return JSONResponse(content=response_data)

        uvicorn.run(self.app, host='0.0.0.0', port=6008)


if __name__ == "__main__":
    log_dir = "/home/app/log"
    os.makedirs(log_dir,exist_ok=True)
    log_path = os.path.join(log_dir,"log.txt")
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s|%(levelname)s|%(thread)d|%(name)s-%(lineno)d| - %(message)s",
        handlers=[logging.FileHandler(filename=log_path, encoding='utf-8', mode='a+'),
                  logging.StreamHandler()]
    )
    logger = logging.getLogger(__name__)
    try:
        my_api = MyAPI()
        my_api.start()
    except Exception as e:
        logger.info(f"API启动失败！\n报错：\n{e}")

