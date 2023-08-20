import threading
import websocket
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

STATUS_FIRST_FRAME = 0
STATUS_CONTINUE_FRAME = 1
STATUS_LAST_FRAME = 2


class SpeechRecognition(object):
    def __init__(self, APPID, APIKey, APISecret):
        self.APPID = APPID
        self.APIKey = APIKey
        self.APISecret = APISecret
        self.running = False
        self.thread = None

        self.CommonArgs = {"app_id": self.APPID}
        self.BusinessArgs = {"domain": "iat", "language": "zh_cn", "accent": "mandarin", "vinfo": 1, "vad_eos": 10000}

    def create_url(self):
        url = 'wss://ws-api.xfyun.cn/v2/iat'
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        signature_origin = "host: " + "ws-api.xfyun.cn" + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + "/v2/iat " + "HTTP/1.1"

        signature_sha = hmac.new(self.APISecret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()
        signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')

        authorization_origin = "api_key=\"%s\", algorithm=\"%s\", headers=\"%s\", signature=\"%s\"" % (
            self.APIKey, "hmac-sha256", "host date request-line", signature_sha)
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')

        v = {
            "authorization": authorization,
            "date": date,
            "host": "ws-api.xfyun.cn"
        }

        url = url + '?' + urlencode(v)
        return url

    def on_message(self, ws, message):
        try:
            code = json.loads(message)["code"]
            sid = json.loads(message)["sid"]
            if code != 0:
                errMsg = json.loads(message)["message"]
                print("sid:%s call error:%s code is:%s" % (sid, errMsg, code))
            else:
                data = json.loads(message)["data"]["result"]["ws"]
                result = ""
                for i in data:
                    for w in i["cw"]:
                        result += w["w"]

                if result == '。' or result == '.。' or result == ' .。' or result == ' 。':
                    pass
                else:
                    print("翻译结果: %s。" % (result))

        except Exception as e:
            print("receive msg,but parse exception:", e)

    def on_error(self, ws, error):
        print("### error:", error)
        self.stop_recognition()

    def on_close(self, ws, close_status_code, close_msg):
        self.stop_recognition()

    def on_open(self, ws):
        def run(*args):
            status = STATUS_FIRST_FRAME
            CHUNK = 520
            FORMAT = pyaudio.paInt16
            CHANNELS = 1
            RATE = 16000
            p = pyaudio.PyAudio()
            stream = p.open(format=FORMAT,
                            channels=CHANNELS,
                            rate=RATE,
                            input=True,
                            frames_per_buffer=CHUNK)

            print("- - - - - - - Start Recording ...- - - - - - - ")

            for i in range(0, int(RATE / CHUNK * 60)):
                buf = stream.read(CHUNK)
                if not buf:
                    status = STATUS_LAST_FRAME
                if status == STATUS_FIRST_FRAME:
                    d = {"common": self.CommonArgs,
                         "business": self.BusinessArgs,
                         "data": {"status": 0, "format": "audio/L16;rate=16000",
                                  "audio": str(base64.b64encode(buf), 'utf-8'),
                                  "encoding": "raw"}}
                    d = json.dumps(d)
                    ws.send(d)
                    status = STATUS_CONTINUE_FRAME
                elif status == STATUS_CONTINUE_FRAME:
                    d = {"data": {"status": 1, "format": "audio/L16;rate=16000",
                                  "audio": str(base64.b64encode(buf), 'utf-8'),
                                  "encoding": "raw"}}
                    ws.send(json.dumps(d))
                elif status == STATUS_LAST_FRAME:
                    d = {"data": {"status": 2, "format": "audio/L16;rate=16000",
                                  "audio": str(base64.b64encode(buf), 'utf-8'),
                                  "encoding": "raw"}}
                    ws.send(json.dumps(d))
                    time.sleep(1)
                    break

        thread.start_new_thread(run, ())

    def run_recognition(self):
        websocket.enableTrace(False)
        wsUrl = self.create_url()
        ws = websocket.WebSocketApp(wsUrl, on_message=self.on_message, on_error=self.on_error, on_close=self.on_close)
        ws.on_open = self.on_open
        ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE}, ping_timeout=2)

    def start_recognition(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self.run_recognition)
            self.thread.start()

    def stop_recognition(self):
        if self.running:
            self.running = False
            if self.thread:
                self.thread.join()

# 示例用法
if __name__ == "__main__":
    wsParam = SpeechRecognition(
        APPID='8b78ee8d',
        APIKey='deb208978c5ae4773f02b1f035a0f1b8',
        APISecret='MjMxZDVhNzE1OGE2MmU4MmNlNzEwNjYx'
    )

    a = threading.Thread(target=wsParam.start_recognition)
    a.start()

    time.sleep(10)  # 运行 10 秒钟
    wsParam.stop_recognition()
