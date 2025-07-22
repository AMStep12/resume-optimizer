# app.py
import streamlit as st

st.set_page_config(page_title="Resume Optimizer", layout="centered")

st.sidebar.title("📂 Navigation")
page = st.sidebar.radio("Go to", [
    "📄 Upload Resume",
    "🧪 Analyze Resume",
    "📥 Generate PDF Report"
])

if page == "📄 Upload Resume":
    import upload_resume
    upload_resume.run()

elif page == "🧪 Analyze Resume":
    import analyze_resume
    analyze_resume.run()

elif page == "📥 Generate PDF Report":
    import report_export
    report_export.run()
