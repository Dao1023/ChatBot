from src import iflytek_iat_demo
from src import SparkDesk_test
from src import pyttsx3_demo
from src import iflytek_tts_demo


while 1:
    
    # 文本输入
    # qustion = 'hello'
    # qustion = input("Dao: ")
    
    # 音频输入
    qustion = iflytek_iat_demo.run()
    print("Dao: ", qustion)

    # 处理
    answer = SparkDesk_test.getAnswer(qustion)
    # answer = "你们好呀"
    
    # 文本输出
    print("SparkDesk: ", answer)

    # 音频输出
    # win32com.client.Dispatch("SAPI.SpVoice").Speak(answer)
    # pyttsx3_demo.speak(answer)
    iflytek_tts_demo.Ws_Param(answer)