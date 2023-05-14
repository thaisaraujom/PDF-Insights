# PDF Insights 👁️📄

This project allows users to upload PDF files and ask questions about them. It leverages various libraries and APIs to extract text from PDFs, split the text into chunks, create embeddings, and perform question-answering tasks.

## 📝 Overview

The code provides a web interface for analyzing PDF files. Here's how it works:

1. Enter your OpenAI API key in the provided input field.

2. Upload one or multiple PDF files using the file uploader.

3. Click the "Process PDFs" button to extract text from the uploaded PDFs and create an indexed knowledge base.

4. Once the PDFs are processed, you can ask questions about the content using the text input field.

5. After entering a question, the code will search the knowledge base for relevant information and provide an answer.

## 📋 Requirements

Make sure you have the following dependencies and libraries installed:

- streamlit==1.22.0
- tiktoken==0.3.3
- PyPDF2==3.0.1
- openai==0.27.2
- langchain==0.0.167
- faiss-cpu==1.7.4
- streamlit-chat==0.0.2.2

You can install the required libraries by running the following command:
```
pip install -r requirements.txt
```

Additionally, you need to have an OpenAI API key. If you don't have one, you can sign up for an account at [OpenAI](https://openai.com/) and obtain an API key from the dashboard.

## 💻 How to Run

1. Clone this repository to your local machine:
    ```
    git clone https://github.com/thaisaraujo2000/PDF-Insights.git
    ```

2. Install the required dependencies as mentioned in the Requirements section.

3. Set your OpenAI API key as an environment variable or enter it when prompted.

4. Run the code using the following command:
    ```
    streamlit run app.py
    ```

5. A Streamlit application will open in your default web browser.

## ℹ️ Additional Information

- Only PDF files are supported for processing.

- The code splits the extracted text into smaller chunks to improve the question-answering performance.

- You can ask questions about the PDF content by entering them in the provided text input field.

- The code displays the generated answer in the Streamlit interface.

- The code uses a spinner to indicate processing or thinking time during PDF extraction and question-answering tasks.

- Make sure to keep your OpenAI API key secure and do not share it with others.

Feel free to explore and analyze different PDFs using this code!