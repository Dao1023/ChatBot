'''
Streamlit 没有前后端分离，但其本身更像是前端框架
main.py 相对于写前端，后端在 src
React 这样的前端框架，在开发环境时用自带的服务器，打包到生产环境用 Nginx 这样的服务器
Streamlit 前端就不封装一层 Web 服务器了，直接拿来用
至于为什么不用前端框架，是因为 Streamlit 学会了以后可以自己开发 Web
'''

from src import SparkDesk_test
from src import message_log
import streamlit as st


def send(user_input):
    message_log.append(f"Dao: {user_input}\n\n")
    message_log.append(f"Bot: {SparkDesk_test.getAnswer(user_input)}\n\n")
    st.write(message_log.read())

def clear():
    message_log.clear()


def main():
    user_input = st.text_input("Enter something:")

    if st.button("Clear"):
        clear()
    
    if st.button("send"):
        send(user_input)

if __name__ == "__main__":
    main()
