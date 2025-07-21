import streamlit as st

st.set_page_config(page_title="Resume Optimizer", layout="centered")
st.title("📄 GPT-Powered Resume Optimizer")
st.write("Upload your resume and paste a job description. Let AI help you stand out!")

uploaded_file = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"])
job_description = st.text_area("Paste the job description you're targeting")

if uploaded_file and job_description:
    st.success("Resume and Job Description are ready to be analyzed!")

