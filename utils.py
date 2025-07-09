import os
import requests
from dotenv import load_dotenv
from fpdf import FPDF

load_dotenv()

# GROQ API details
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL_NAME = "llama3-70b-8192"

headers = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}


def clean_response(content: str) -> str:
    """Remove unwanted boilerplate from start or end."""
    content = content.strip()

    # Remove starting boilerplate
    if content.lower().startswith("here is a professional"):
        content = content.split("\n", 1)[1]

    # Remove any polite or ending messages
    unwanted_endings = [
        "I hope this helps",
        "Let me know if you need anything else",
        "Note:",
        "This resume was generated",
        "Hope this helps",
        "Best regards",
    ]

    for phrase in unwanted_endings:
        if phrase in content:
            content = content.split(phrase)[0].strip()

    return content


def generate_resume(name, email, phone, job_title, company, experience, skills, education, linkedin_url):
    prompt = f"""
Write a professional and complete resume in markdown format using the following details:

Full Name: {name}
Email: {email}
Phone: {phone}
Job Title: {job_title}
Company: {company}
Experience: {experience}
Skills: {skills}
Education: {education}
LinkedIn: {linkedin_url if linkedin_url else 'N/A'}

The resume should include:
- Header with name and contact
- Objective for job role at the company
- Education
- Experience
- Skills
"""

    response = requests.post(GROQ_URL, headers=headers, json={
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    })

    try:
        content = response.json()["choices"][0]["message"]["content"].strip()
        content = clean_response(content)
        print("✅ Resume Content:", content[:300])
        return content
    except Exception as e:
        print("❌ Error in resume generation:", e)
        print("Full API Response:", response.text)
        return "❌ Failed to generate resume. Check API key or quota."


def generate_cover_letter(name, email, phone, job_title, company, experience, skills, education):
    prompt = f"""
Write a formal, enthusiastic cover letter in markdown format using these details:

Full Name: {name}
Email: {email}
Phone: {phone}
Job Title: {job_title}
Company: {company}
Experience: {experience}
Skills: {skills}
Education: {education}

Make it personalized, 3 paragraphs, ending with a strong closing.
"""

    response = requests.post(GROQ_URL, headers=headers, json={
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    })

    try:
        content = response.json()["choices"][0]["message"]["content"].strip()
        content = clean_response(content)
        print("✅ Cover Letter Content:", content[:300])
        return content
    except Exception as e:
        print("❌ Error in cover letter generation:", e)
        print("Full API Response:", response.text)
        return "❌ Failed to generate cover letter."


def convert_to_pdf(content_md, output_file="output.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    lines = content_md.strip().split('\n')
    for line in lines:
        pdf.multi_cell(0, 10, txt=line, align="L")

    pdf_bytes = pdf.output(dest='S').encode('latin-1')
    return pdf_bytes
