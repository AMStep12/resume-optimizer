
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
You are an AI resume reviewer. Compare the following resume to the job description. 

Score each of these categories from 0–10:
- Skills Match
- Keyword Match
- Experience Relevance
- Role Alignment
- Formatting & Clarity

Output the scores in this exact format:
Skills Match: #
Keyword Match: #
Experience Relevance: #
Role Alignment: #
Formatting & Clarity: #

Then follow with your improvement suggestions and one-paragraph summary.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}
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
                st.markdown("### 📋 Feedback")
                st.markdown(output)


            except Exception as e:
                st.error(f"Error calling OpenAI API: {e}")

