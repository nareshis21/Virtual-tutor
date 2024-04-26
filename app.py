import streamlit as st
from src.audio import audio_d
from src.chat import virtual_tutor
from src.OCR import I_OCR
from utils.qa import chain
import numpy as np
import pandas as pd
import easyocr
from PIL import Image
import cv2
from utils.qa import chain
import base64
from src.about import virtual_tutor_markdown as sms
from src.pdf_up import process_uploaded_file
from src.pdf import pdf_v
from langchain.memory import ConversationBufferWindowMemory
from langchain_community.chat_message_histories import StreamlitChatMessageHistory

memory_storage = StreamlitChatMessageHistory(key="chat_messages")
memory = ConversationBufferWindowMemory(memory_key="chat_history", human_prefix="User", chat_memory=memory_storage, k=3)
image_bg = r".\image\freepik-export-20240425023906eVmL.jpeg"

def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(f"""<style>.stApp {{background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
    background-size: cover}}</style>""", unsafe_allow_html=True)
add_bg_from_local(image_bg)

def get_answer(query):
    response = chain.invoke(query)
    #return response["result"]
    return response
 
# Page 1: Home Page
def home():
    st.header("Welcome")
    #st.set_page_config(layout='wide', page_title="Virtual Tutor")
    st.markdown("""
        <svg width="600" height="100">
            <text x="50%" y="50%" font-family="San serif" font-size="42px" fill="Black" text-anchor="middle" stroke="white"
             stroke-width="0.3" stroke-linejoin="round">Virtual Tutor - CHAT
            </text>
        </svg>
    """, unsafe_allow_html=True)

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hi! How may I assist you today?"}
        ]

    st.markdown("""
        <style> 
        .stChatInputContainer > div {
        background-color: #000000;
        }
        </style>
        """, unsafe_allow_html=True)

    for message in st.session_state.messages: # Display the prior chat messages
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

# Page 2: About Page
#def Virtual_CHAT():
#    st.header("Welcome chat")
# Page 3: Contact Page
def Image_Query():
    I_OCR()

def Audio():
    audio_d()

def pdf_():
    process_uploaded_file()

def About():
    st.markdown(sms)
# Page Selector
def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Go to", ["Home", "Image Query","Audio","PDF","ABOUT US"])

    if page == "Home":
        virtual_tutor()
    #elif page == "Virtual Chat":
    #    home()
    elif page == "Image Query":
        Image_Query()
    elif page == "Audio":
        audio_d()
    elif page == "PDF":
        pdf_()
    elif page == "ABOUT US":
        About()

    if st.sidebar.button("Clear Chat History"):
        memory_storage.clear()
        st.session_state.clear()

if __name__ == "__main__":
    main()
