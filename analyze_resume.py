# analyze_resume.py
import streamlit as st
import openai
from openai import OpenAI
import re
import io
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
from utils import extract_text_from_pdf, extract_text_from_docx

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def run():
    st.title("🧪 Analyze Resume")

    if not all(k in st.session_state for k in ["uploaded_file", "job_title", "company_name", "job_description"]):
        st.warning("Please go to '📄 Upload Resume' first.")
        return

    resume_file = st.session_state.uploaded_file

    if resume_file.name.endswith(".pdf"):
        resume_text = extract_text_from_pdf(resume_file)
    else:
        resume_text = extract_text_from_docx(resume_file)

    st.session_state.resume_text = resume_text

    if st.button("🔍 Analyze Resume"):
        try:
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
{resume_text}

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
            """labels = categories
            num_vars = len(labels)
            angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()

            # Make the radar loop by repeating the first value at the end
            scores_plot = scores + scores[:1]
            angles_plot = angles + angles[:1]
            labels_plot = labels + labels[:1]  # for safety, not always needed

            fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
            ax.plot(angles_plot, scores_plot, color='blue', linewidth=2)
            ax.fill(angles_plot, scores_plot, color='skyblue', alpha=0.4)
            ax.set_yticks([2, 4, 6, 8, 10])
            ax.set_yticklabels(['2', '4', '6', '8', '10'])
            ax.set_xticks(angles)
            ax.set_xticklabels(labels)
            ax.set_title("ATS Resume Match Breakdown", size=14, y=1.08)

            st.pyplot(fig)"""

            st.write("Scores extracted from GPT:", scores)

            # Debugging test plot
            scores_plot = [6, 7, 8, 5, 6]
            labels = ["Skills Match", "Keyword Match", "Experience", "Alignment", "Clarity"]
            angles = np.linspace(0, 2 * np.pi, len(scores_plot), endpoint=False).tolist()
            scores_plot += scores_plot[:1]
            angles += angles[:1]
            
            fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
            ax.plot(angles, scores_plot, color='red', linewidth=2)
            ax.fill(angles, scores_plot, color='red', alpha=0.25)
            ax.set_xticks(angles[:-1])
            ax.set_xticklabels(labels)
            ax.set_yticks([2, 4, 6, 8, 10])
            ax.set_title("DEBUG: Radar Chart")
            
            st.pyplot(fig)

            chart_buffer = BytesIO()
            fig.savefig(chart_buffer, format="png")
            chart_buffer.seek(0)
            st.session_state.chart_image = chart_buffer.getvalue()  # <-- this returns raw PNG bytes


            st.markdown("### 📋 Feedback")
            st.markdown(output)

        except Exception as e:
            st.error(f"Something went wrong during analysis. Error: {e}")
