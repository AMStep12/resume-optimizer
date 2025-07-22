# report_export.py
import streamlit as st
from fpdf import FPDF
from PIL import Image
from io import BytesIO

def generate_pdf(chart_img_bytes, feedback_text, job_title, company_name):
    pdf = FPDF()
    pdf.add_page()

    # Header
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Resume Optimization Report", ln=True, align='C')
    pdf.ln(10)

    # Job Info
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, f"Job Title: {job_title}", ln=True)
    pdf.cell(0, 10, f"Company: {company_name}", ln=True)
    pdf.ln(10)

    # Chart Image
    image = Image.open(chart_img_bytes)
    temp_path = "/tmp/chart.png"
    image.save(temp_path)
    pdf.image(temp_path, x=30, y=None, w=150)
    pdf.ln(85)

    # Feedback
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "AI Feedback", ln=True)
    pdf.set_font("Arial", '', 11)
    for line in feedback_text.split("\n"):
        pdf.multi_cell(0, 8, line)

    # Output as buffer
    pdf_buffer = BytesIO()
    pdf.output(pdf_buffer)
    pdf_buffer.seek(0)
    return pdf_buffer

def run():
    st.title("📥 Download Resume Report")

    if not all(k in st.session_state for k in ["feedback_text", "chart_image", "job_title", "company_name"]):
        st.warning("⚠️ You need to analyze a resume first on the 'Analyze Resume' page.")
        return

    # Display summary info
    st.write(f"**Job Title:** {st.session_state.job_title}")
    st.write(f"**Company Name:** {st.session_state.company_name}")
    st.markdown("### 📋 Feedback Preview")
    st.markdown(st.session_state.feedback_text)

    # Generate PDF
    pdf_file = generate_pdf(
        st.session_state.chart_image,
        st.session_state.feedback_text,
        st.session_state.job_title,
        st.session_state.company_name
    )

    # Download button
    st.download_button(
        label="📥 Download PDF Report",
        data=pdf_file,
        file_name="resume_analysis_report.pdf",
        mime="application/pdf"
    )
