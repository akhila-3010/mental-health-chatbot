# -*- coding: utf-8 -*-
"""Untitled2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1mz_lCZ4F1gKHh1ka9rf6Z5jahNFx4PdD
"""

!pip install langchain_groq langchain_core langchain_community

!pip install langchain_groq

from langchain_groq import ChatGroq
llm=ChatGroq(
    temperature=0,
    groq_api_key="//",
    model_name="llama-3.3-70b-versatile"
)
result=llm.invoke("Who is lord Ram?")
print(result.content)

!pip install -U langchain chromadb sentence-transformers

import os
os.environ["CHROMA_TELEMETRY"] = "False"

from langchain.vectorstores import Chroma

pip install --upgrade chromadb

pip install -U langchain langchain-community chromadb sentence-transformers langchain-groq

import os
os.environ["CHROMA_TELEMETRY"] = "False"

import logging
logging.getLogger("chromadb.telemetry").setLevel(logging.CRITICAL)

from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_groq import ChatGroq

def initialize_llm():
    llm = ChatGroq(
        temperature=0,
        groq_api_key="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",  # Replace with env variable ideally
        model_name="llama3-70b-8192"  # Correct Groq model name (use official Groq supported models)
    )
    return llm

def create_vector_db():
    loader = DirectoryLoader("/content/data", glob="*.pdf", loader_cls=PyPDFLoader)
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = text_splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    vector_db = Chroma.from_documents(
        texts,
        embeddings,
        persist_directory="./chroma_db"
    )
    print("✅ Chroma DB created and data saved.")
    return vector_db

def setup_qa_chain(vector_db, llm):
    retriever = vector_db.as_retriever()
    prompt_template = """You are a compassionate mental health chatbot. Respond thoughtfully to the following question:
    Context: {context}
    User: {question}
    Chatbot:"""
    PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        chain_type_kwargs={"prompt": PROMPT}
    )
    return qa_chain

def main():
    print("Initializing Chatbot..........")
    llm = initialize_llm()

    db_path = "/content/chroma_db"

    if not os.path.exists(db_path):
        vector_db = create_vector_db()
    else:
        embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
        vector_db = Chroma(persist_directory=db_path, embedding_function=embeddings)

    qa_chain = setup_qa_chain(vector_db, llm)

    while True:
        query = input("\nHuman: ")
        if query.lower() == "exit":
            print("Chatbot: Take Care of yourself, Goodbye!")
            break
        response = qa_chain.run(query)
        print(f"Chatbot: {response}")

if __name__ == "__main__":
    main()



import os
os.environ["CHROMA_TELEMETRY"] = "False"

import logging
logging.getLogger("chromadb.telemetry").setLevel(logging.CRITICAL)

from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_groq import ChatGroq
import gradio as gr  # Make sure you installed `langchain-groq`

def initialize_llm():
    llm = ChatGroq(
        temperature=0,
        groq_api_key="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",  # Replace with env variable ideally
        model_name="llama3-70b-8192"  # Correct Groq model name (use official Groq supported models)
    )
    return llm

def create_vector_db():
    loader = DirectoryLoader("/content/data", glob="*.pdf", loader_cls=PyPDFLoader)
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = text_splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    vector_db = Chroma.from_documents(
        texts,
        embeddings,
        persist_directory="./chroma_db"
    )
    print("✅ Chroma DB created and data saved.")
    return vector_db

def setup_qa_chain(vector_db, llm):
    retriever = vector_db.as_retriever()
    prompt_template = """You are a compassionate mental health chatbot. Respond thoughtfully to the following question:
    Context: {context}
    User: {question}
    Chatbot:"""
    PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        chain_type_kwargs={"prompt": PROMPT}
    )
    return qa_chain

print("Initializing Chatbot..........")
llm = initialize_llm()

db_path = "/content/chroma_db"

if not os.path.exists(db_path):
  vector_db = create_vector_db()
else:
  embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
  vector_db = Chroma(persist_directory=db_path, embedding_function=embeddings)
qa_chain = setup_qa_chain(vector_db, llm)

import gradio as gr

def chatbot_response(message, history):
    global qa_chain

    if not message.strip():
        return history + [{"role": "assistant", "content": "Please provide a valid input."}]

    try:
        # Run your QA chain
        response = qa_chain.run(message)
        # Append to history in OpenAI-style message format
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": response})
        return history
    except Exception as e:
        history.append({"role": "assistant", "content": f"⚠️ Error: {str(e)}"})
        return history

# Build the Gradio App
with gr.Blocks(theme="Respair/Shiki@1.2.1") as app:
    gr.Markdown("# 🧠 Mental Health Chatbot 🤖")
    gr.Markdown("A compassionate chatbot designed to assist with mental well-being. "
                "Please note: For serious concerns, contact a mental health professional.")

    gr.ChatInterface(
        fn=chatbot_response,
        title="Mental Health Chatbot",
        chatbot=gr.Chatbot(type="messages"),  # 👈 use OpenAI-style message dicts
    )

    gr.Markdown("This chatbot provides general support. For urgent issues, seek help from licensed professionals.")

# Launch the app with full support
app.launch(share=True, debug=True, pwa=True)

gradio deploy

pip install gradio_client

from gradio_client import Client

client = Client("https://02dcf2f7c0efc66d5f.gradio.live/")
result = client.predict(
		message="Hello!!",
		api_name="/chat"
)
print(result)

!pip install gradio

# Install the recommended package

create_vector_db()

!pip install -U langchain-huggingface

!pip install sentence_transformers

!pip install sentence_transformers

"""# New Section"""

!pip install chromadb

!pip install pypdf

!pip install langchain_groq langchain_core langchain_community

!pip install -U langchain-huggingface sentence-transformers chromadb



create_vector_db()

!pip install langchain_groq langchain_core langchain_community langchain

!pip install chromadb

!pip install sentence-transformers

!pip install langchain-huggingface

!pip install pypdf

# Commented out IPython magic to ensure Python compatibility.
# %pip install pypdf