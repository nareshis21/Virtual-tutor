import streamlit as st
import base64
from utils.qa import chain
from langchain.memory import ConversationBufferWindowMemory
from langchain_community.chat_message_histories import StreamlitChatMessageHistory

def virtual_tutor():
    #st.set_page_config(layout='wide')
    #st.set_page_config(page_title="Virtual Tutor")

    st.markdown("""
        <svg width="600" height="100">
            <text x="50%" y="50%" font-family="San serif" font-size="42px" fill="Black" text-anchor="middle" stroke="white"
             stroke-width="0.3" stroke-linejoin="round">Virtual Tutor - CHAT
            </text>
        </svg>
    """, unsafe_allow_html=True)

    def add_bg_from_local(image_file):
        with open(image_file, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
        st.markdown(
            f"""<style>.stApp {{background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
            background-size: cover}}</style>""",
            unsafe_allow_html=True)

    #add_bg_from_local(r'C:\Users\Naresh Kumar Lahajal\Desktop\Capstone-streamlit\STREAMCHAT\freepik-export-20240425023906eVmL.jpeg')

    def initialize_session_state():
        if "messages" not in st.session_state:
            st.session_state.messages = [
                {"role": "assistant", "content": "Hi! How may I assist you today?"}
            ]

    initialize_session_state()

    m = st.markdown("""
        <style> 
        .stChatInputContainer > div {
        background-color: #000000;
        }
        </style>
        """, unsafe_allow_html=True)

    def get_answer(query):
        response = chain.invoke(query)
        return response

    memory_storage = StreamlitChatMessageHistory(key="chat_messages")
    memory = ConversationBufferWindowMemory(memory_key="chat_history", human_prefix="User", chat_memory=memory_storage, k=3)

    for message in st.session_state.messages:  # Display the prior chat messages
        with st.chat_message(message["role"]):
            st.write(message["content"])

    for i, msg in enumerate(memory_storage.messages):
        name = "user" if i % 2 == 0 else "assistant"
        st.chat_message(name).markdown(msg.content)

    if user_input := st.chat_input("User Input"):
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.spinner("Generating Response..."):

            with st.chat_message("assistant"):
                response = get_answer(user_input)
                answer = response['result']
                st.markdown(answer)
                message = {"role": "assistant", "content": answer}
                message_u = {"role": "user", "content": user_input}
                st.session_state.messages.append(message_u)
                st.session_state.messages.append(message)


#virtual_tutor()
