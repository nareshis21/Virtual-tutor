import streamlit as st
import os
import base64
from audio_recorder_streamlit import audio_recorder
from streamlit_float import *
from utils.stt import speech_to_text
from utils.tts import text_to_speech
from utils.qa import chain

recorded_audio = r".\media\recorded.mp3"
output_audio = r".\media\ouput_file.mp3"

def autoplay_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode("utf-8")
    md = f"""
    <audio autoplay>
    <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
    </audio>
    """
    st.markdown(md, unsafe_allow_html=True)

def get_answer(query):
    response = chain.invoke(query)
    return response['result']

def audio_d():
    float_init()

    st.title("Ai Doubt resolver")

    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hi! How may I assist you today?"}
        ]

    footer_container = st.container()

    with footer_container:
        audio_bytes = audio_recorder()

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    if audio_bytes:
        with st.spinner("Transcribing..."):
            webm_file_path = recorded_audio
            with open(webm_file_path, "wb") as f:
                f.write(audio_bytes)

            transcript = speech_to_text()
            if transcript:
                st.session_state.messages.append({"role": "user", "content": transcript})
                with st.chat_message("user"):
                    st.write(transcript)

    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking🤔..."):
                final_response = get_answer(str(st.session_state.messages))
            with st.spinner("Generating audio response..."):    
                text_to_speech(final_response)
                audio_file = output_audio
                autoplay_audio(audio_file)
            st.write(final_response)
            st.session_state.messages.append({"role": "assistant", "content": final_response})
            os.remove(audio_file)

    # Float the footer container and provide CSS to target it with
    footer_container.float("bottom: 0rem;")
