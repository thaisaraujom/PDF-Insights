# 📖 PDF Insights

This project allows users to upload PDF files and ask questions about them. It leverages various libraries and APIs to extract text from PDFs, split the text into chunks, create embeddings, and perform question-answering tasks. Now, with the addition of a feature that allows exporting the chat history to a PDF file.

## 🌟 Features

- Upload PDFs and get answers about their contents.
- Utilize various libraries and APIs for text extraction and analysis.
- Export the entire chat history to a PDF file.

## 📝 Overview

This project provides a web interface for analyzing PDF files. Here's how it works:

1. **Setup**: Enter your OpenAI API key in the provided field.
2. **Upload**: Add one or multiple PDF files using the file uploader.
3. **Processing**: Click "Process PDFs" to extract text and create an indexed knowledge base.
4. **Query**: After processing, ask questions about the content.
5. **Answers**: Receive relevant information from the database.
6. **Export**: Save the entire chat conversation to a PDF file.

## 📋 Prerequisites

- Install the necessary libraries:
    ```bash
    pip install -r requirements.txt
    ```

- Have an OpenAI API key. [Sign up at OpenAI](https://openai.com/) if you don’t have one.

## 💻 How to Run

1. **Clone** the repository:
    ```bash
    git clone https://github.com/thaisaraujom/PDF-Insights.git
    ```

2. **Install** the dependencies.
3. **Set** your OpenAI API key as an environment variable or input it when prompted.
4. **Run** the code:
    ```bash
    streamlit run app.py
    ```

The Streamlit application will open in your default web browser.

## ℹ️ Additional Information

- 📄 Supports PDF files only.
- 📜 Extracted text is broken down into smaller chunks to enhance performance.
- ❓ Ask questions using the provided text input field.
- 🔄 A spinner is displayed during extraction or questioning tasks.
- 🔒 Keep your OpenAI API key secure.

**Explore and analyze different PDFs using this code!**
