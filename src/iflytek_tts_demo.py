import websocket
import datetime
import hashlib
import base64
import hmac
import json
from urllib.parse import urlencode
import time
import ssl
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime
import _thread as thread
import os
import yaml


class Ws_Param(object):
    # 初始化
    def __init__(self, Text="你好，世界", file_name=r"conf\iflytek.yaml"):
        with open(file_name, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            self.APPID = data["appid"]
            self.APIKey = data["api_key"]
            self.APISecret = data["api_secret"]
            self.pcm_path = data['tts_pcm']
        
        self.Text = Text

        # 公共参数(common)
        self.CommonArgs = {"app_id": self.APPID}
        # 业务参数(business)，更多个性化参数可在官网查看
        self.BusinessArgs = {"aue": "raw", "auf": "audio/L16;rate=16000", "vcn": "xiaoyan", "tte": "utf8", "speed": 100}
        self.Data = {"status": 2, "text": str(base64.b64encode(self.Text.encode('utf-8')), "UTF8")}
        #使用小语种须使用以下方式，此处的unicode指的是 utf16小端的编码方式，即"UTF-16LE"”
        #self.Data = {"status": 2, "text": str(base64.b64encode(self.Text.encode('utf-16')), "UTF8")}

        self.run()

    # 生成url
    def create_url(self):
        url = 'wss://tts-api.xfyun.cn/v2/tts'
        # 生成RFC1123格式的时间戳
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        # 拼接字符串
        signature_origin = "host: " + "ws-api.xfyun.cn" + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + "/v2/tts " + "HTTP/1.1"
        # 进行hmac-sha256进行加密
        signature_sha = hmac.new(self.APISecret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()
        signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')

        authorization_origin = "api_key=\"%s\", algorithm=\"%s\", headers=\"%s\", signature=\"%s\"" % (
            self.APIKey, "hmac-sha256", "host date request-line", signature_sha)
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
        # 将请求的鉴权参数组合为字典
        v = {
            "authorization": authorization,
            "date": date,
            "host": "ws-api.xfyun.cn"
        }
        # 拼接鉴权参数，生成url
        url = url + '?' + urlencode(v)
        # print("date: ",date)
        # print("v: ",v)
        # 此处打印出建立连接时候的url,参考本demo的时候可取消上方打印的注释，比对相同参数时生成的url与自己代码生成的url是否一致
        # print('websocket url :', url)
        return url
        
    # 提取 WebSocket 消息保存为 pcm 音频文件
    def on_message(self, message):
        try:
            message =json.loads(message)
            code = message["code"]
            sid = message["sid"]
            audio = message["data"]["audio"]
            audio = base64.b64decode(audio)
            status = message["data"]["status"]
            
            # print(message)
            # with open('message.json', 'w', encoding='utf-8') as f:
            #     f.write(json.dumps(message))
            
            if status == 2:
                # print("ws is closed")
                self.ws.close()
            if code != 0:
                errMsg = message["message"]
                print("sid:%s call error:%s code is:%s" % (sid, errMsg, code))
            else:
                with open(self.pcm_path, 'ab') as f:
                    f.write(audio)

        except Exception as e:
            print("receive msg,but parse exception:", e)

    # 收到websocket错误的处理
    def on_error(self, error):
        # print("### error:", error)
        pass

    # 收到websocket关闭的处理
    def on_close(self):
        # print("### closed ###")
        pass

    # 收到websocket连接建立的处理
    def on_open(self):
        def run(*args):
            d = {
                    "common": self.CommonArgs,
                    "business": self.BusinessArgs,
                    "data": self.Data,
                }
            d = json.dumps(d)
            # print("------>开始发送文本数据")
            self.ws.send(d)
            if os.path.exists(self.pcm_path):
                os.remove(self.pcm_path)

        thread.start_new_thread(run, ())

    def run(self):
        websocket.enableTrace(False)
        self.wsUrl = self.create_url()
        self.ws = websocket.WebSocketApp(self.wsUrl, on_message=self.on_message, on_error=self.on_error, on_close=self.on_close)
        self.ws.on_open = self.on_open
        self.ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
        
        os.system(f'ffplay -nodisp -autoexit -ar 16000 -channels 1 -f s16le -i {self.pcm_path} > NUL 2>&1')

if __name__ == "__main__":
    client = Ws_Param("今天吃了吗")