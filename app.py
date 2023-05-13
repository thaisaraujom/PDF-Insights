import os
import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback

def main():
    # Initialize session_state variables if they don't exist
    if 'pdfs_processed' not in st.session_state:
        st.session_state.pdfs_processed = False
    if 'knowledge_base' not in st.session_state:
        st.session_state.knowledge_base = None

    openai_key = st.text_input('Enter your OpenAI API key:', type='password', key='openai_key')
    st.header('PDF Insights')

    if openai_key:
        os.environ["OPENAI_API_KEY"] = openai_key
        st.success('API key provided.')

        pdfs = st.file_uploader('Choose PDF files', type=['pdf'], accept_multiple_files=True)

        # Add a button to confirm PDF processing
        process_pdfs = st.button('Process PDFs')

        # Extract text from the uploaded PDF
        if process_pdfs and pdfs and not st.session_state.pdfs_processed:
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

        if st.session_state.pdfs_processed:
            # Placeholder for question input
            question_placeholder = st.empty()

            # Show user input
            user_question = question_placeholder.text_input('Ask a question about your PDF:', key='text_input')

            if user_question:
                with st.spinner('Thinking...'):  # add spinner here
                    docs = st.session_state.knowledge_base.similarity_search(user_question)

                    llm = OpenAI()
                    chain = load_qa_chain(llm, chain_type="stuff")
                    with get_openai_callback() as cb:
                        response = chain.run(input_documents=docs, question=user_question)
                        print(cb)

                st.write(response)  # Display the response from the chatbot

    else:
        st.warning('Please enter your OpenAI API key.')


if __name__ == '__main__':
    main()
