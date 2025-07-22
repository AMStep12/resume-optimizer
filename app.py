
import streamlit as st
import openai
from openai import OpenAI
from utils import extract_text_from_pdf, extract_text_from_docx
import re
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
from fpdf import FPDF
from PIL import Image

# 🔐 Secure API client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# 🖼 Streamlit UI
st.set_page_config(page_title="Resume Optimizer", layout="centered")
st.title("📄 GPT-Powered Resume Optimizer")
st.write("Upload your resume, enter job details, and get a personalized optimization report.")

# 🧾 Inputs
job_title = st.text_input("🎯 Target Job Title", placeholder="e.g. Data Analyst")
company_name = st.text_input("🏢 Company Name", placeholder="e.g. Amazon")
uploaded_file = st.file_uploader("📤 Upload your resume (PDF or DOCX)", type=["pdf", "docx"])
job_description = st.text_area("📝 Paste the job description")

# 🧠 GPT prompt builder
def build_prompt(resume_text, job_description):
    return f"""
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

Then follow with your improvement suggestions and a one-paragraph summary.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}
"""

# 🧾 PDF generator
def generate_pdf(chart_img, feedback_text, job_title, company_name):
    pdf = FPDF()
    pdf.add_page()

    # Title Page Info
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Resume Optimization Report", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, f"Job Title: {job_title}", ln=True)
    pdf.cell(0, 10, f"Company: {company_name}", ln=True)
    pdf.ln(10)

    # Chart Image
    image = Image.open(chart_img)
    image_path = "/tmp/chart.png"
    image.save(image_path)
    pdf.image(image_path, x=30, y=None, w=150)
    pdf.ln(85)

    # Feedback
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "AI Feedback", ln=True)
    pdf.set_font("Arial", '', 11)
    for line in feedback_text.split("\n"):
        pdf.multi_cell(0, 8, line)

    # Return buffer
    pdf_buffer = BytesIO()
    pdf.output(pdf_buffer)
    pdf_buffer.seek(0)
    return pdf_buffer

# 🔁 Resume processing
if uploaded_file and job_description and job_title and company_name:
    if uploaded_file.name.endswith(".pdf"):
        resume_text = extract_text_from_pdf(uploaded_file)
    else:
        resume_text = extract_text_from_docx(uploaded_file)

    st.success("Resume, job info, and job description loaded!")

    if st.button("🔍 Analyze Resume"):
        try:
            with st.spinner("Analyzing with GPT..."):
                
        except Exception as e:
        st.error(f"Something went wrong during processing. Error: {e}")

            try:
                prompt = build_prompt(resume_text, job_description)
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful resume optimization assistant."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.5
                )
                output = response.choices[0].message.content

                # 📊 Extract scores
                categories = ["Skills Match", "Keyword Match", "Experience Relevance", "Role Alignment", "Formatting & Clarity"]
                scores = []
                for category in categories:
                    match = re.search(rf"{category}:\s*(\d+)", output)
                    if match:
                        scores.append(int(match.group(1)))
                    else:
                        scores.append(0)

                # 🕸 Radar chart
                labels = categories
                num_vars = len(labels)
                scores += scores[:1]
                angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
                angles += angles[:1]
                fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
               import streamlit as st
import openai
from openai import OpenAI
from utils import extract_text_from_pdf, extract_text_from_docx
import re
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
from fpdf import FPDF
from PIL import Image

# Secure API client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="Resume Optimizer", layout="centered")
st.title("📄 GPT-Powered Resume Optimizer")
st.write("Upload your resume, enter job details, and get a personalized optimization report.")

# Inputs
job_title = st.text_input("🎯 Target Job Title", placeholder="e.g. Data Analyst")
company_name = st.text_input("🏢 Company Name", placeholder="e.g. Amazon")
uploaded_file = st.file_uploader("📤 Upload your resume (PDF or DOCX)", type=["pdf", "docx"])
job_description = st.text_area("📝 Paste the job description")

# GPT prompt builder
def build_prompt(resume_text, job_description):
    return f"""
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

Then follow with your improvement suggestions and a one-paragraph summary.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}
"""

# PDF generator
def generate_pdf(chart_img, feedback_text, job_title, company_name):
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Resume Optimization Report", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, f"Job Title: {job_title}", ln=True)
    pdf.cell(0, 10, f"Company: {company_name}", ln=True)
    pdf.ln(10)

    image = Image.open(chart_img)
    image_path = "/tmp/chart.png"
    image.save(image_path)
    pdf.image(image_path, x=30, y=None, w=150)
    pdf.ln(85)

    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "AI Feedback", ln=True)
    pdf.set_font("Arial", '', 11)
    for line in feedback_text.split("\n"):
        pdf.multi_cell(0, 8, line)

    pdf_buffer = BytesIO()
    pdf.output(pdf_buffer)
    pdf_buffer.seek(0)
    return pdf_buffer

# Process resume if everything is filled
if uploaded_file and job_description and job_title and company_name:
    st.write("Uploaded file:", uploaded_file.name)

    try:
        if uploaded_file.name.endswith(".pdf"):
            resume_text = extract_text_from_pdf(uploaded_file)
        else:
            resume_text = extract_text_from_docx(uploaded_file)

        st.success("Resume, job info, and job description loaded!")

        if st.button("🔍 Analyze Resume"):
            try:
                with st.spinner("Analyzing with GPT..."):
                    prompt = build_prompt(resume_text, job_description)
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "You are a helpful resume optimization assistant."},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.5
                    )

                    output = response.choices[0].message.content

                    # Extract scores
                    categories = ["Skills Match", "Keyword Match", "Experience Relevance", "Role Alignment", "Formatting & Clarity"]
                    scores = []
                    for category in categories:
                        match = re.search(rf"{category}:\s*(\d+)", output)
                        if match:
                            scores.append(int(match.group(1)))
                        else:
                            scores.append(0)

                    # Radar chart
                    labels = categories
                    num_vars = len(labels)
                    scores += scores[:1]
                    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
                    angles += angles[:1]

                    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
                    ax.plot(angles, scores, color='blue', linewidth=2)
                    ax.fill(angles, scores, color='skyblue', alpha=0.4)
                    ax.set_yticks([2, 4, 6, 8, 10])
                    ax.set_yticklabels(['2', '4', '6', '8', '10'])
                    ax.set_xticks(angles[:-1])
                    ax.set_xticklabels(labels)
                    ax.set_title("ATS Resume Match Breakdown", size=14, y=1.08)
                    st.pyplot(fig)

                    # Feedback
                    st.markdown("### 📋 Feedback")
                    st.markdown(output)

                    # Save chart image
                    chart_buffer = BytesIO()
                    fig.savefig(chart_buffer, format="png")
                    chart_buffer.seek(0)

                    # Generate and download PDF
                    pdf_file = generate_pdf(chart_buffer, output, job_title, company_name)
                    st.download_button(
                        label="📥 Download PDF Report",
                        data=pdf_file,
                        file_name="resume_analysis_report.pdf",
                        mime="application/pdf"
                    )

            except Exception as e:
                st.error(f"Something went wrong during pr

