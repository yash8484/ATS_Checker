from dotenv import load_dotenv
import base64
import streamlit as st
import os
import io
from PIL import Image
import pdf2image
import google.generativeai as genai
import PyPDF2 as pdf

# Load environment variables
load_dotenv()

# Set up API key securely
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    st.error("Google API key not found. Please set it in .env or Streamlit Secrets.")
else:
    genai.configure(api_key=API_KEY)

# Function to process PDF and extract text
def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page_text = reader.pages[page].extract_text()
        if page_text:
            text += page_text + "\n"
    return text.strip() if text else "No text extracted from PDF."

# Function to get response from Gemini API
def get_gemini_response(input_text):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(input_text)
    return response.text

# Streamlit App
st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")

input_text = st.text_area("Job Description:", key="input")
uploaded_file = st.file_uploader("Upload your resume (PDF)...", type=["pdf"])

if uploaded_file is not None:
    st.write("✅ PDF Uploaded Successfully")

submit1 = st.button("Tell Me About the Resume")
submit3 = st.button("Percentage Match")

input_prompt1 = f"""
You are an experienced Technical HR Manager. Review the resume against the job description.
Highlight strengths, weaknesses, and overall suitability.

Resume:
{text}

Job Description:
{input_text}
"""

input_prompt3 = f"""
You are an ATS scanner with expertise in AI and data science hiring.
Evaluate the resume for a job match percentage, missing keywords, and improvements.

Resume:
{text}

Job Description:
{input_text}
"""

if submit1:
    if uploaded_file is not None:
        try:
            extracted_text = input_pdf_text(uploaded_file)
            response = get_gemini_response(input_prompt1.format(text=extracted_text))
            st.subheader("The Response is:")
            st.write(response)
        except Exception as e:
            st.error(f"❌ An error occurred: {e}")
    else:
        st.write("⚠️ Please upload a resume")

elif submit3:
    if uploaded_file is not None:
        try:
            extracted_text = input_pdf_text(uploaded_file)
            response = get_gemini_response(input_prompt3.format(text=extracted_text))
            st.subheader("The Response is:")
            st.write(response)
        except Exception as e:
            st.error(f"❌ An error occurred: {e}")
    else:
        st.write("⚠️ Please upload a resume")
