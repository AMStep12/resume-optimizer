
import streamlit as st
import openai
from utils import extract_text_from_pdf, extract_text_from_docx
import re
import matplotlib.pyplot as plt
import numpy as np

# 👉 REPLACE THIS WITH YOUR ACTUAL API KEY
openai.api_key = st.secrets.get("OPENAI_API_KEY", "sk-...your-key-here...")

st.set_page_config(page_title="Resume Optimizer", layout="centered")
st.title("📄 GPT-Powered Resume Optimizer")
st.write("Upload your resume and paste a job description. Let AI help you stand out!")

uploaded_file = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"])
job_description = st.text_area("Paste the job description you're targeting")

if uploaded_file and job_description:
    # Extract text from uploaded resume
    if uploaded_file.name.endswith(".pdf"):
        resume_text = extract_text_from_pdf(uploaded_file)
    else:
        resume_text = extract_text_from_docx(uploaded_file)

    st.success("Resume and Job Description loaded!")

    if st.button("🔍 Analyze Resume"):
        with st.spinner("Analyzing with GPT..."):

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

Then follow with your improvement suggestions and one-paragraph summary.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}
"""


            try:
                client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful resume optimization assistant."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.5
                )

                output = response.choices[0].message.content
                

# Parse category scores from GPT response
categories = ["Skills Match", "Keyword Match", "Experience Relevance", "Role Alignment", "Formatting & Clarity"]
scores = []

for category in categories:
    match = re.search(rf"{category}:\s*(\d+)", output)
    if match:
        scores.append(int(match.group(1)))
    else:
        scores.append(0)  # default if missing

# Close radar loop
scores += scores[:1]
labels = categories + categories[:1]

# Radar chart
angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
scores = np.array(scores)
angles += angles[:1]

fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
ax.plot(angles, scores, color='blue', linewidth=2)
ax.fill(angles, scores, color='skyblue', alpha=0.4)
ax.set_yticks([2, 4, 6, 8, 10])
ax.set_yticklabels(['2', '4', '6', '8', '10'])
ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories)
ax.set_title("ATS Resume Match Breakdown", size=14, y=1.08)

st.pyplot(fig)

                st.markdown("### 📋 Feedback")
                st.markdown(output)


            except Exception as e:
                st.error(f"Error calling OpenAI API: {e}")

