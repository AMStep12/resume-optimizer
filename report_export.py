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

    for line in feedback_text.sp_

