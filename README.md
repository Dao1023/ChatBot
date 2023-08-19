## 一个语音机器人的测试

本项目适合新手学习

项目简单，结构清晰，适合快速搭建聊天机器人服务
- conf：配置文件
- data：生成的音频临时文件
- src：程序文件
  - 输入：语音输入、文本输入
  - 处理：讯飞大语言模型
  - 输出：文本输出、语音输出
- main.py：程序入口

使用 Python，且各组件间模块化处理，可以单独移植
- 比如加个 streamlit 做一个 WebUI，可以快速展示
- 比如加个 docker 部署到服务器上，各大云服务器新用户一般一年 100 块钱

（想想就激动）

同时，我也上传了自己的 iflytek.yaml 配置文件， token 虽然不多，但可以供大家玩
现在讯飞申请很快，且免费额度不少，大家自己去注册一下就能替换掉我的 APPID 等配置了

## 使用方法

以下安装方式仅供参考

git

```shell
git clone https://github.com/Dao1023/ChatBot
cd ChatBot
```

pip

```shell
pip install xxx
python main.py
```

conda（推荐）

```shell
conda create -n ChatBot python=3.10
conda activate ChatBot
conda install pyaudio xxx xxx xxx
# pip install xxx xxx xxx
python main.py
```