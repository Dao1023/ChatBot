from src import SparkDesk_test
import streamlit as st

st.title("Chatbot Interface")

# 使用streamlit的session_state来存储聊天历史
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# 用户输入
user_input = st.text_input("Your Question:")
if st.button('Send'):
    if user_input:
        # 获取回答
        answer = SparkDesk_test.getAnswer(user_input)
        st.session_state.chat_history.append(("You", user_input))
        st.session_state.chat_history.append(("Bot", answer))

# 显示聊天历史
for role, message in st.session_state.chat_history:
    if role == "You":
        st.write(f"You: {message}")
    else:
        st.write(f"Bot: {message}")
