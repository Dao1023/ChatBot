FROM python:3.8-slim
WORKDIR /app
COPY . /app
RUN pip3 install -r requirements.txt
# RUN pip install xxx -i https://mirrors.aliyun.com/pypi/simple # 国内速度慢用这个
CMD ["streamlit", "run", "main.py"]
