# upload_resume.py
import streamlit as st
from utils import extract_text_from_pdf, extract_text_from_docx

def run():
    st.title("📄 Upload Resume")
    st.write("Upload your resume and fill in the job info.")

    job_title = st.text_input("🎯 Target Job Title", placeholder="e.g. Data Analyst")
    company_name = st.text_input("🏢 Company Name", placeholder="e.g. Amazon")
    uploaded_file = st.file_uploader("📤 Upload your resume (PDF or DOCX)", type=["pdf", "docx"])
    job_description = st.text_area("📝 Paste the job description")

    if uploaded_file:
        st.session_state.uploaded_file = uploaded_file
        st.success("Resume uploaded successfully.")

    if job_title:
        st.session_state.job_title = job_title

    if company_name:
        st.session_state.company_name = company_name

    if job_description:
        st.session_state.job_description = job_description

    if uploaded_file and job_title and company_name and job_description:
        st.success("✅ All set! You can now go to '🧪 Analyze Resume'")
