## 开发手册

### 第一次修改

2023年8月20日：

- 改正linux所需的依赖，放在requirement.txt中

- 解决websocket无法使用的问题

- 解决了linux端无法使用语音识别功能的问题

- 语音识别功能放在了speech to text

- 将语音识别demo改进成了一个类为SpeechRecognition类

- 可以通过实理化SpeechRecognition类，完成语音的开始和停止

  ```python
  # 实例化SpeechRecognition类
  wsParam = SpeechRecognition(
      APPID='8b78ee8d',
      APIKey='deb208978c5ae4773f02b1f035a0f1b8',
      APISecret='MjMxZDVhNzE1OGE2MmU4MmNlNzEwNjYx'
  )
  
  # 开始语音识别
  wsParam.start_recognition()
  
  # 让程序运行一段时间
  time.sleep(10)  # 运行 10 秒钟
  
  # 停止语音识别
  wsParam.stop_recognition()
  
  ```

  

