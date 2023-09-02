FROM python:3.8-slim
WORKDIR /app
COPY . /app
# RUN pip3 install -r requirements.txt
# 国内速度慢用这个
RUN pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple
CMD ["streamlit", "run", "main.py"]
