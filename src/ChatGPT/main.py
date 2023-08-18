import openai
import yaml


def get_answer(prompt, api_key):
    openai.api_key = api_key
    chat_log = openai.Completion.create(
        engine="gpt-3.5-turbo",
        prompt=prompt,
        max_tokens=100,
    )
    return chat_log['choices'][0]['text']

def yaml_read(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
        return data

def run():
    try:
        # 读取配置文件
        account = yaml_read(r'conf\account.yaml')
        api_key = account['api_key']
        prompt = input('提问：')

        # 发起请求
        answer = get_answer(prompt, api_key)
        print(answer)
    except Exception as e:
        error_message = str(e)
        print("发生错误:", error_message)

run()