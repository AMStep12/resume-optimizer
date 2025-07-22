
import streamlit as st
import openai
from utils import extract_text_from_pdf, extract_text_from_docx

# 👉 REPLACE THIS WITH YOUR ACTUAL API KEY
openai.api_key = st.secrets.get("OPENAI_API_KEY", "sk-...your-key-here...")

st.set_page_config(page_title="Resume Optimizer", layout="centered")
st.title("📄 GPT-Powered Resume Optimizer")
st.write("Upload your resume and paste a job description. Let AI help you stand out!")

uploaded_file = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"])
job_description = st.text_area("Paste the job description you're targeting")

if uploaded_file and job_description:
    # Extract text from uploaded resume
    if uploaded_file.name.endswith(".pdf"):
        resume_text = extract_text_from_pdf(uploaded_file)
    else:
        resume_text = extract_text_from_docx(uploaded_file)

    st.success("Resume and Job Description loaded!")

    if st.button("🔍 Analyze Resume"):
        with st.spinner("Analyzing with GPT..."):

            prompt = f"""
You are an expert resume coach. Analyze the resume below and compare it to the job description. 
Provide improvement suggestions, missing keywords, and highlight strengths and weaknesses. 

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Return your answer in this format:
1. Bullet point suggestions for improvement
2. One paragraph summary
"""

            try:
                client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful resume optimization assistant."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.5
                )

                output = response.choices[0].message.content


            except Exception as e:
                st.error(f"Error calling OpenAI API: {e}")

