import os
from typing import List
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import Qdrant
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from qdrant_client import QdrantClient
from langchain_community.chat_models import ChatOllama


#import chainlit as cl
from langchain.chains import RetrievalQA

# bring in our GROQ_API_KEY
from dotenv import load_dotenv
load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
qdrant_url = os.getenv("QDRANT_URL")
qdrant_api_key = os.getenv("QDRANT_API_KEY")

custom_prompt_template = """Use the following pieces of information to answer the user's question.
If you don't know the answer, just say that you don't know,if it is out of context say that it is out of context and also try to provide the answer and don't be rude.

Context: {context}
Question: {question}

Only return the helpful answer below and nothing else.
Helpful answer:
"""

def set_custom_prompt():
    """
    Prompt template for QA retrieval for each vectorstore
    """
    prompt = PromptTemplate(template=custom_prompt_template,
                            input_variables=['context', 'question'])
    return prompt


chat_model = ChatGroq(temperature=0, model_name="mixtral-8x7b-32768")
#chat_model = ChatGroq(temperature=0, model_name="Llama2-70b-4096")
#chat_model = ChatOllama(model="llama2", request_timeout=30.0)

client = QdrantClient(api_key=qdrant_api_key, url=qdrant_url,)


def retrieval_qa_chain(llm, prompt, vectorstore):
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(search_kwargs={'k': 2}),
        return_source_documents=True,
        chain_type_kwargs={'prompt': prompt}
    )
    return qa_chain


def qa_bot():
    embeddings = FastEmbedEmbeddings()
    vectorstore = Qdrant(client=client, embeddings=embeddings, collection_name="rag")
    llm = chat_model
    qa_prompt=set_custom_prompt()
    qa = retrieval_qa_chain(llm, qa_prompt, vectorstore)
    return qa

#---------------------------------------------------------------------#
 
#qdrant_cloud_api_key="your_qdrant_cloud_api_key"
#qdrant_url="your_qdrant_url"

#qdrant_cloud = Qdrant.from_documents(
#    docs,
#   embeddings,
#   url=qdrant_url,
#   prefer_grpc=True,
#   api_key=qdrant_cloud_api_key,
#  collection_name="qdrant_cloud_documents",
#)

#---------------------------------------------------------------------#
query="how to make coffee"
print(query)

chain = qa_bot()


