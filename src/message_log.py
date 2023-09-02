# 追加消息记录
def append(msg):
    with open("data/message.txt", "a", encoding="utf-8") as f:
        f.write(msg)

# 读取消息记录
def read():
    with open("data/message.txt", "r", encoding="utf-8") as f:
        return f.read()

# 清空消息记录
def clear():
    with open("data/message.txt", "w", encoding="utf-8") as f:
        f.write("")