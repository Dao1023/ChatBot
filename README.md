## 一个语音机器人的测试

本项目是 WebUI 版本的分支

项目简单，结构清晰，适合快速搭建聊天机器人服务
- conf：配置文件
- data：生成的音频临时文件
- src：程序文件
  - 输入：文本输入
  - 处理：讯飞大语言模型
  - 输出：文本输出
- main.py：程序入口

使用 Python，且各组件间模块化处理，可以单独移植
- 比如加个 streamlit 做一个 WebUI，可以快速展示
- 比如加个 docker 部署到服务器上，各大云服务器新用户一般一年 100 块钱

同时，我也上传了自己的 iflytek.yaml 配置文件， token 虽然不多，但可以供大家玩

现在讯飞申请很快，且免费额度不少，大家自己去注册一下就能替换掉我的 APPID 等配置了

## 使用方法

### 开发环境

git

```shell
git clone https://github.com/Dao1023/ChatBot.git
cd ChatBot
git checkout streamlit

```

Python（推荐 conda 环境）

```shell
conda create -n ChatBot python=3.10
conda activate ChatBot
```

安装 Python 依赖

```shell
pip install -r requirements.txt
```

启动程序

```shell
streamlit run main.py
```
### 生产环境

git

```shell
git clone https://github.com/Dao1023/ChatBot.git
cd ChatBot
git checkout streamlit
```

docker

```shell
docker build -t chatbot .
docker run -p 80:8501 chatbot
```
