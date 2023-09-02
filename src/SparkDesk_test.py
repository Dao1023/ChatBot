from . import SparkApi
import yaml


text =[]
# length = 0

def yaml_read(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

# 载入参数
iflytek = yaml_read(r"conf\iflytek.yaml")
appid = iflytek["appid"]
api_key = iflytek["api_key"]
api_secret = iflytek["api_secret"]
Spark_url = iflytek["Spark_url"]
domain = iflytek["domain"]


def getText(role,content):
    jsoncon = {"role": role, "content": content}
    text.append(jsoncon)
    return text

def getlength(text):
    return sum(len(content["content"]) for content in text)

def checklen(text):
    while (getlength(text) > 8000):
        del text[0]
    return text

def getAnswer(Input):
    question = checklen(getText("user",Input))
    SparkApi.answer =""
    SparkApi.main(appid,api_key,api_secret,Spark_url,domain,question)
    getText("assistant",SparkApi.answer)
    answer = question[1]['content']
    question.clear()
    return answer

# 当此文件为主模块时才会执行
if __name__ == "__main__":
    while(1):
        Input = input("你：")
        print("星火：", getAnswer(Input))