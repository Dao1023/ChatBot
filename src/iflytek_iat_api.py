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
import pyaudio
import yaml


def audio_record(out_file, rec_time):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16  # 16bit编码格式
    CHANNELS = 1  # 单声道
    RATE = 16000  # 16000采样频率

    p = pyaudio.PyAudio()
    # 创建音频流
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("Start Recording...")
    frames = []  # 录制的音频流
    # 录制音频数据
    for i in range(0, int(RATE / CHUNK * rec_time)):
        data = stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    # 保存音频文件为PCM格式
    with open(out_file, 'wb') as f:
        for frame in frames:
            f.write(frame)

STATUS_FIRST_FRAME = 0  # 第一帧的标识
STATUS_CONTINUE_FRAME = 1  # 中间帧标识
STATUS_LAST_FRAME = 2  # 最后一帧的标识


class Ws_Param(object):
    # 初始化
    def __init__(self, file_name="config/iflytek.yaml"):
        with open(file_name, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            self.APPID = data["appid"]
            self.APIKey = data["api_key"]
            self.APISecret = data["api_secret"]
            self.AudioFile = data['iat_pcm']
            self.result = ""

        # 公共参数(common)
        self.CommonArgs = {"app_id": self.APPID}
        # 业务参数(business)，更多个性化参数可在官网查看
        self.BusinessArgs = {"domain": "iat", "language": "zh_cn", "accent": "mandarin", "vinfo":1,"vad_eos":10000}

    # 生成url
    def create_url(self):
        url = 'wss://ws-api.xfyun.cn/v2/iat'
        # 生成RFC1123格式的时间戳
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        # 拼接字符串
        signature_origin = "host: " + "ws-api.xfyun.cn" + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + "/v2/iat " + "HTTP/1.1"
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

    # 收到websocket消息的处理
    def on_message(self, message):
        try:
            code = json.loads(message)["code"]
            sid = json.loads(message)["sid"]
            if code != 0:
                errMsg = json.loads(message)["message"]
                print("sid:%s call error:%s code is:%s" % (sid, errMsg, code))

            else:
                data = json.loads(message)["data"]["result"]["ws"]
                # print(json.loads(message))
                # self.result = ""
                for i in data:
                    for w in i["cw"]:
                        self.result += w["w"]
                # print("sid:%s call success!,data is:%s" % (sid, json.dumps(data, ensure_ascii=False)))
                # print(self.result)
        except Exception as e:
            print("receive msg,but parse exception:", e)

    # 收到websocket错误的处理
    def on_error(self, error):
        # print("### error:", error)
        pass

    # 收到websocket关闭的处理
    def on_close(self,a,b):
        # print("### closed ###")
        pass

    # 收到websocket连接建立的处理
    def on_open(self):
        def run(*args):
            frameSize = 8000  # 每一帧的音频大小
            intervel = 0.04  # 发送音频间隔(单位:s)
            status = STATUS_FIRST_FRAME  # 音频的状态信息，标识音频是第一帧，还是中间帧、最后一帧

            with open(self.AudioFile, "rb") as fp:
                while True:
                    buf = fp.read(frameSize)
                    # 文件结束
                    if not buf:
                        status = STATUS_LAST_FRAME
                    # 第一帧处理
                    # 发送第一帧音频，带business 参数
                    # appid 必须带上，只需第一帧发送
                    if status == STATUS_FIRST_FRAME:

                        d = {"common": self.CommonArgs,
                            "business": self.BusinessArgs,
                            "data": {"status": 0, "format": "audio/L16;rate=16000",
                                    "audio": str(base64.b64encode(buf), 'utf-8'),
                                    "encoding": "raw"}}
                        d = json.dumps(d)
                        self.ws.send(d)
                        status = STATUS_CONTINUE_FRAME
                    # 中间帧处理
                    elif status == STATUS_CONTINUE_FRAME:
                        d = {"data": {"status": 1, "format": "audio/L16;rate=16000",
                                    "audio": str(base64.b64encode(buf), 'utf-8'),
                                    "encoding": "raw"}}
                        self.ws.send(json.dumps(d))
                    # 最后一帧处理
                    elif status == STATUS_LAST_FRAME:
                        d = {"data": {"status": 2, "format": "audio/L16;rate=16000",
                                    "audio": str(base64.b64encode(buf), 'utf-8'),
                                    "encoding": "raw"}}
                        self.ws.send(json.dumps(d))
                        time.sleep(1)
                        break
                    # 模拟音频采样间隔
                    time.sleep(intervel)
            self.ws.close()

        thread.start_new_thread(run, ())

    def run(self):
        # 保存音频临时文件
        audio_record(self.AudioFile, 3)

        # 测速
        # time1 = datetime.now()

        websocket.enableTrace(False)
        self.wsUrl = self.create_url()
        self.ws = websocket.WebSocketApp(self.wsUrl, on_message=self.on_message, on_error=self.on_error, on_close=self.on_close)
        self.ws.on_open = self.on_open
        self.ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
        
        # time2 = datetime.now()
        # print(time2-time1)

        return self.result

if __name__ == "__main__":
    ws = Ws_Param()
    result = ws.run()
    print(result)