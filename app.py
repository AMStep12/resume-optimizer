# app.py
import streamlit as st

# Page navigation
st.set_page_config(page_title="Resume Optimizer", layout="centered")

st.sidebar.title("📂 Navigation")
page = st.sidebar.radio("Go to", ["🧪 Analyze Resume", "📄 Generate PDF Report"])

if page == "🧪 Analyze Resume":
    import resume_analysis
    resume_analysis.run()

elif page == "📄 Generate PDF Report":
    import report_export
    report_export.run()
