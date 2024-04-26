import streamlit as st
from streamlit import session_state as ss
from langchain.memory import ConversationBufferWindowMemory, StreamlitChatMessageHistory
from streamlit_pdf_viewer import pdf_viewer
from utils.qa import chain

def get_answer(query):
    response = chain.invoke(query)
    return response['result']

def pdf_v():
    # Declare variable.
    if 'pdf_ref' not in ss:
        ss.pdf_ref = None

    # Access the uploaded ref via a key.
    st.file_uploader("Upload PDF file", type=('pdf'), key='pdf')

    if ss.pdf:
        ss.pdf_ref = ss.pdf  # backup

    # Now you can access "pdf_ref" anywhere in your app.
    if ss.pdf_ref:
        binary_data = ss.pdf_ref.getvalue()
        pdf_viewer(input=binary_data, width=700)

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

