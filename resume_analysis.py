# resume_analysis.py
import streamlit as st
import openai
from openai import OpenAI
from utils import extract_text_from_pdf, extract_text_from_docx
import re
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def run():
    st.title("🧪 Resume Analysis")
    st.write("Upload your resume, fill in job info, and analyze alignment.")

    job_title = st.text_input("🎯 Target Job Title", placeholder="e.g. Data Analyst")
    company_name = st.text_input("🏢 Company Name", placeholder="e.g. Amazon")
    uploaded_file = st.file_uploader("📤 Upload your resume (PDF or DOCX)", type=["pdf", "docx"])
    job_description = st.text_area("📝 Paste the job description")

    if uploaded_file:
        st.session_state.uploaded_file = uploaded_file
        st.success("Resume uploaded. Ready to analyze.")
        st.session_state.file_uploaded = True

    if (
        st.session_state.get("file_uploaded")
        and job_title
        and company_name
        and job_description
    ):
        if st.button("🔍 Analyze Resume"):
            try:
                resume_file = st.session_state.uploaded_file
                if resume_file.name.endswith(".pdf"):
                    resume_text = extract_text_from_pdf(resume_file)
                else:
                    resume_text = extract_text_from_docx(resume_file)

                st.session_state.resume_text = resume_text
                st.session_state.job_title = job_title
                st.session_state.company_name = company_name
                st.session_state.job_description = job_description

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

Then follow with your improvement suggestions and a one-paragraph summary.

RESUME:
{st.session_state.resume_text}

JOB DESCRIPTION:
{st.session_state.job_description}
"""

                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful resume optimization assistant."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.5
                )

                output = response.choices[0].message.content
                st.session_state.feedback = output
                st.session_state.feedback_text = output

                # Extract scores
                categories = [
                    "Skills Match",
                    "Keyword Match",
                    "Experience Relevance",
                    "Role Alignment",
                    "Formatting & Clarity"
                ]
                scores = []

                for category in categories:
                    match = re.search(rf"{category}:\\s*(\\d+)", output)
                    scores.append(int(match.group(1)) if match else 0)

                st.session_state.chart_scores = scores

                # Radar chart
                labels = categories
                num_vars = len(labels)
                angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
                scores += scores[:1]
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

                chart_buffer = BytesIO()
                fig.savefig(chart_buffer, format="png")
                chart_buffer.seek(0)
                st.session_state.chart_image = chart_buffer

                st.markdown("### 📋 Feedback")
                st.markdown(output)

            except Exception as e:
                st.error(f"Something went wrong during analysis. Error: {e}")
    else:
        st.info("Upload resume and complete all fields to analyze.")
