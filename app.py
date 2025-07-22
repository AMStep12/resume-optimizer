# app.py
import streamlit as st

# 🔐 Maintenance toggle
if st.secrets.get("APP_ACTIVE") != "true":
    st.markdown("### 🚧 This app is temporarily offline for updates.")
    st.text_input("🔐 Enter access password", type="password", disabled=True)
    st.stop()

# 🔑 Password gate
password = st.text_input("🔐 Enter access password", type="password")
if password != st.secrets.get("APP_PASSWORD"):
    st.warning("Access denied. Please enter the correct password")

    
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

# 📬 Footer contact info
st.sidebar.markdown("---")
st.sidebar.caption("Built by Aaron Stephenson")
st.sidebar.caption("📬 caringzulu5@gmail.com")
