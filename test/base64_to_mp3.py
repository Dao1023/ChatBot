# base64 转 mp3
import base64
import os
import sys
import json

def json_read(file):
    with open(file, 'r') as f:
        return json.load(f)

message = json_read(r'test\message.json')

audio = message["data"]["audio"]
audio = base64.b64decode(audio)

with open(r'data\demo.pcm', 'ab') as f:
    f.write(audio)

os.system('ffplay -nodisp -ar 16000 -channels 1 -f s16le -i test\demo.pcm')