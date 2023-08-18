from SparkDesk import SparkDesk_test
from tts import pyttsx3_demo
from tts_ws import tts_ws_python3_demo

# 输入
# qustion = 'hello'
# print(qustion)

# 处理
# answer = SparkDesk_test.getAnswer("讯飞真是一个可爱的工具呢")
answer = "你们好呀"

# 输出
print(answer)
# pyttsx3_demo.speak(answer)
tts_ws_python3_demo.run(answer)