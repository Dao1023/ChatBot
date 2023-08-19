from . import SparkApi
import yaml


text =[]
# length = 0

def yaml_read(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
        return data

# 载入参数
iflytek = yaml_read(r"conf\iflytek.yaml")
appid = iflytek["appid"]
api_key = iflytek["api_key"]
api_secret = iflytek["api_secret"]
Spark_url = iflytek["Spark_url"]
domain = iflytek["domain"]


def getText(role,content):
    jsoncon = {}
    jsoncon["role"] = role
    jsoncon["content"] = content
    text.append(jsoncon)
    return text

def getlength(text):
    length = 0
    for content in text:
        temp = content["content"]
        leng = len(temp)
        length += leng
    return length

def checklen(text):
    while (getlength(text) > 8000):
        del text[0]
    return text

def getAnswer(question):
    text.clear
    Input = question
    question = checklen(getText("user",Input))
    SparkApi.answer =""
    SparkApi.main(appid,api_key,api_secret,Spark_url,domain,question)
    getText("assistant",SparkApi.answer)
    
    return text[1]['content']

# 当此文件为主模块时才会执行
if __name__ == "__main__":
    text.clear
    while(1):
        Input = input("\n" +"我:")
        question = checklen(getText("user",Input))
        SparkApi.answer =""
        print("星火:",end = "")
        SparkApi.main(appid,api_key,api_secret,Spark_url,domain,question)
        getText("assistant",SparkApi.answer)
        print(text[1]['content'])
