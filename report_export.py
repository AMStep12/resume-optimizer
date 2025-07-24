import streamlit as st
from fpdf import FPDF
import io
from PIL import Image

def generate_pdf(chart_img, feedback_text, job_title, company_name):
    pdf = FPDF()
    pdf.add_page()

    # Title section
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "GPT Resume Feedback Report", ln=True, align="C")

    pdf.set_font("Arial", "", 12)
    pdf.ln(10)
    pdf.cell(0, 10, f"Job Title: {job_title}", ln=True)
    pdf.cell(0, 10, f"Company: {company_name}", ln=True)

    # Insert radar chart
    pdf.ln(10)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "ATS Score Breakdown", ln=True)

    if chart_img:
        img = Image.open(io.BytesIO(chart_img))
        img_path = "/tmp/chart.png"
        img.save(img_path)
        pdf.image(img_path, x=40, y=None, w=130)

    # Add feedback text
    pdf.ln(10)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "AI Feedback & Suggestions", ln=True)
    pdf.ln(5)
    pdf.set_font("Arial", "", 11)

    for line in feedback_text.split("\n"):
        pdf.multi_cell(0, 8, line)

    # Export PDF as bytes
    pdf_output = pdf.output(dest="S").encode("latin-1")
    return pdf_output

def run():
    st.title("📄 Export Resume Feedback as PDF")

    if "feedback" not in st.session_state:
        st.warning("Please run an analysis first on the main page.")
        return

    if st.button("📥 Generate PDF Report"):
        pdf_file = generate_pdf(
            st.session_state.chart_image,
            st.session_state.feedback,
            st.session_state.job_title,
            st.session_state.company_name
        )

        st.download_button(
            label="📄 Download PDF",
            data=pdf_file,
            file_name="resume_feedback.pdf",
            mime="application/pdf"
        )
