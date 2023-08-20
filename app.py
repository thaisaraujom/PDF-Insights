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
from io import BytesIO
import base64


from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.units import inch
from reportlab.platypus.flowables import Image
from PIL import Image as PilImage
from reportlab.platypus import Spacer


def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if 'pdfs_processed' not in st.session_state:
        st.session_state.pdfs_processed = False
    if 'knowledge_base' not in st.session_state:
        st.session_state.knowledge_base = None
    if 'messages' not in st.session_state:
        st.session_state.messages = deque(maxlen=6)  # Only keep the 10 most recent messages
    if 'all_messages' not in st.session_state:  # create a new list for all messages
        st.session_state.all_messages = []

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
    st.session_state.all_messages.append({'message': question, 'is_user': True})  # Add user question to the all_messages list


    with st.spinner('Thinking...'):
        docs = st.session_state.knowledge_base.similarity_search(question)

        llm = OpenAI()
        chain = load_qa_chain(llm, chain_type="stuff")
        with get_openai_callback() as cb:
            response = chain.run(input_documents=docs, question=question)
            print(cb)

    st.session_state.messages.append({'message': response, 'is_user': False})  # Add bot response to the message list
    st.session_state.all_messages.append({'message': response, 'is_user': False})  # Add bot response to the all_messages list

def on_page(canvas, doc):
    # This function will be called for each page during the PDF creation process.
    # It receives a `canvas` object that can be used to draw on the page,
    # and a `doc` object that contains information about the document.
    
    # Add your image file
    img_path = './img/logo.png'
    # Load your image file with PIL
    pil_image = PilImage.open(img_path)

    # Get the original width and height of the image
    orig_width, orig_height = pil_image.size

    # Define the width you want for the image in the PDF
    img_width = 1.0 * inch

    # Calculate the height based on the original image's aspect ratio
    img_height = img_width * orig_height / orig_width

    img = Image(img_path, width=img_width, height=img_height)
    
    # Draw image at the top of the page
    x_position = 1.09 * inch  # adjust as necessary
    img.drawOn(canvas, x_position, doc.height + 1 * inch)  # adjust second and third parameter as necessary

def export_chat_to_pdf():
    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer, pagesize=letter)
    
    story = []
    styles = getSampleStyleSheet()
    style = styles['BodyText']
    style.alignment = 4  # Justify text

    # Add a space after the image
    story.append(Spacer(1, 0.5*inch))  # adjust the second parameter as necessary

    # Add chat messages in pairs, separated by a Spacer
    for i in range(0, len(st.session_state.all_messages), 2):
        user_msg = st.session_state.all_messages[i]
        bot_msg = st.session_state.all_messages[i+1] if i + 1 < len(st.session_state.all_messages) else None

        user_text = 'You: ' + user_msg['message']
        para = Paragraph(user_text, style)
        story.append(para)

        if bot_msg:
            bot_text = 'Bot: ' + bot_msg['message']
            para = Paragraph(bot_text, style)
            story.append(para)

        # Add a Spacer after each user-bot pair
        story.append(Spacer(1, 0.2*inch))  # Adjust the second parameter to control the space height

    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)  # The function `on_page` will be called for each page

    pdf_bytes = buffer.getvalue()
    buffer.close()

    return pdf_bytes


def display_chat():
    """Display the chat messages."""
    for i, msg in enumerate(st.session_state.messages):
        message(msg['message'], is_user=msg['is_user'], key=str(i))

def main():
    initialize_session_state()
    st.title('PDF Insights')
    openai_key = st.text_input('Enter your OpenAI API key:', type='password', key='openai_key')
    if openai_key:
        os.environ["OPENAI_API_KEY"] = openai_key
        st.success('API key provided', icon='✅')
    else:
        st.warning('Please enter your OpenAI API key.', icon='⚠️')
        st.stop()

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
        
        # Only process the question if the Export Chat button has not been pressed
        export_chat_button = st.button('Export Chat')
        if user_question and not export_chat_button:
            answer_question(user_question)
            display_chat()

        # Add a button to export the chat to a PDF file
        if len(st.session_state.all_messages) > 0:  # Display the export button only if there's at least one message
            if export_chat_button:

                # Generate PDF bytes
                pdf_bytes = export_chat_to_pdf()

                # Create a download link
                b64 = base64.b64encode(pdf_bytes).decode()
                linko= f'<a href="data:application/octet-stream;base64,{b64}" download="chat_history.pdf">Click Here to download your PDF file</a>'
                st.markdown(linko, unsafe_allow_html=True)

if __name__ == '__main__':
    main()
