from dotenv import load_dotenv
load_dotenv()  ## Load all the environment variables

import streamlit as st
import os
import google.generativeai as genai
from PyPDF2 import PdfReader
import io

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function to load Google Gemini Pro Vision API And get response
def get_gemini_response(input, text, prompt):
    model = genai.GenerativeModel('gemini-2.0-pro-exp')
    response = model.generate_content([input, text, prompt])
    return response.text

def extract_text_from_pdf(uploaded_file):
    try:
        pdf_reader = PdfReader(io.BytesIO(uploaded_file.read()))
        text = []
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text.append(page.extract_text())
        return "\n".join(text)
    except Exception as e:
        st.error(f"Error reading PDF file: {e}")
        return ""

## Initialize our Streamlit app

st.header("Clinical Lab Report Analyzer")
input = st.text_input("Input Prompt: ", key="input")
uploaded_file = st.file_uploader("Choose a PDF file...", type=["pdf"])

submit = st.button("Analyze Report")

input_prompt = """
You are a clinical lab report analyzer. Analyze the uploaded lab report and discuss only the parameters that are not normal according to Indian health standards. Provide suggestions on diet and recommend which specialists the user should refer to for further treatment.
"""

## If submit button is clicked
if submit:
    if uploaded_file is not None:
        pdf_text = extract_text_from_pdf(uploaded_file)
        if pdf_text:
            response = get_gemini_response(input_prompt, pdf_text, input)
            st.subheader("The Analysis Results")
            st.write(response)
            #st.subheader("Summary")
           # st.write("Overall report summary here...")
