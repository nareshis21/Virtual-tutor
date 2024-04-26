import numpy as np
import pandas as pd
import easyocr
import streamlit as st
from PIL import Image
import cv2
import base64
from utils.qa import chain
from langchain.memory import ConversationBufferWindowMemory
from langchain_community.chat_message_histories import StreamlitChatMessageHistory

def I_OCR():
    # Function to display the OCR image with bounding boxes and text
    def display_ocr_image(img, results):
        img_np = np.array(img)
        for detection in results:
            top_left = tuple([int(val) for val in detection[0][0]])
            bottom_right = tuple([int(val) for val in detection[0][2]])
            text = detection[1]
            font = cv2.FONT_HERSHEY_COMPLEX
            cv2.rectangle(img_np, top_left, bottom_right, (0, 255, 0), 5)
            cv2.putText(img_np, text, top_left, font, 1, (125, 29, 241), 2, cv2.LINE_AA)
        st.image(img_np, channels="BGR", use_column_width=True)

    # Function to extract text from DataFrame column
    def extracted_text(col):
        return " , ".join(img_df[col])

    # Function to initialize session state
    def initialize_session_state():
        if "messages" not in st.session_state:
            st.session_state.messages = [
                {"role": "assistant", "content": "Hi! How may I assist you today?"}
            ]

    # Function to get answer from QA model
    def get_answer(query):
        response = chain.invoke(query)
        return response["result"]

    # Streamlit app
    st.title("Question in image")

    file = st.file_uploader(label= "Upload Image Here (png/jpg/jpeg) : ", type=['png', 'jpg', 'jpeg'])

    if file is not None:
        image = Image.open(file)
        st.image(image)

        reader = easyocr.Reader(['en', 'hi'], gpu=False)
        results = reader.readtext(np.array(image))

        img_df = pd.DataFrame(results, columns=['bbox', 'Predicted Text', 'Prediction Confidence'])

        text_combined = extracted_text(col='Predicted Text')
        st.write("Text Generated :- ", text_combined)

        display_ocr_image(image, results)

    else:
        st.warning("!! Please Upload your image !!")

    initialize_session_state()

    memory_storage = StreamlitChatMessageHistory(key="chat_messages")
    memory = ConversationBufferWindowMemory(memory_key="chat_history", human_prefix="User", chat_memory=memory_storage, k=3)

    for i, msg in enumerate(memory_storage.messages):
        name = "user" if i % 2 == 0 else "assistant"
        st.chat_message(name).markdown(msg.content)

    if user_input := st.chat_input("User Input"):
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.spinner("Generating Response..."):
            with st.chat_message("assistant"):
                response = get_answer(user_input)
                answer = response
                st.markdown(answer)

    #if st.sidebar.button("Clear Chat History"):
    #    memory_storage.clear()

# Run the OCR function
#OCR()
