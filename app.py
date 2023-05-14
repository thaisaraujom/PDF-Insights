import os
import streamlit as st
from streamlit_chat import message
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback
from collections import deque

def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if 'pdfs_processed' not in st.session_state:
        st.session_state.pdfs_processed = False
    if 'knowledge_base' not in st.session_state:
        st.session_state.knowledge_base = None
    if 'messages' not in st.session_state:
        st.session_state.messages = deque(maxlen=6)  # Only keep the 10 most recent messages

def process_pdfs(pdfs):
    """Extract text from PDFs and create a knowledge base."""
    with st.spinner('Processing PDFs...'):
        text = ''
        for pdf in pdfs:
            pdf_reader = PdfReader(pdf)
            for page in pdf_reader.pages:
                text += page.extract_text()

        # Split the text into chunks
        text_splitter = CharacterTextSplitter(
            separator='\n',
            chunk_size=500,
            chunk_overlap=20,
            length_function=len
        )
        chunks = text_splitter.split_text(text)

        # Create embeddings
        embeddings = OpenAIEmbeddings()
        st.session_state.knowledge_base = FAISS.from_texts(chunks, embeddings)

        st.session_state.pdfs_processed = True
        st.success('PDFs processed. You may now ask questions.')

def answer_question(question):
    """Generate an answer to a question using the knowledge base."""
    st.session_state.messages.append({'message': question, 'is_user': True})  # Add user question to the message list
    with st.spinner('Thinking...'):
        docs = st.session_state.knowledge_base.similarity_search(question)

        llm = OpenAI()
        chain = load_qa_chain(llm, chain_type="stuff")
        with get_openai_callback() as cb:
            response = chain.run(input_documents=docs, question=question)
            print(cb)

    st.session_state.messages.append({'message': response, 'is_user': False})  # Add bot response to the message list

def display_chat():
    """Display the chat messages."""
    for i, msg in enumerate(st.session_state.messages):
        message(msg['message'], is_user=msg['is_user'], key=str(i))

def main():
    initialize_session_state()

    openai_key = st.text_input('Enter your OpenAI API key:', type='password', key='openai_key')
    st.header('PDF Insights')

    if openai_key:
        os.environ["OPENAI_API_KEY"] = openai_key
        st.success('API key provided.')

        pdfs = st.file_uploader('Choose PDF files', type=['pdf'], accept_multiple_files=True)

        # Add a button to confirm PDF processing
        process_pdfs_button = st.button('Process PDFs')

        # Extract text from the uploaded PDF
        if process_pdfs_button and pdfs and not st.session_state.pdfs_processed:
            process_pdfs(pdfs)
        
                # Placeholder for question input
        question_placeholder = st.empty()

        if st.session_state.pdfs_processed:
            user_question = question_placeholder.text_input('Ask a question about your PDF:', key='text_input')

            if user_question:
                answer_question(user_question)

            display_chat()

    else:
        st.warning('Please enter your OpenAI API key.')

if __name__ == '__main__':
    main()
