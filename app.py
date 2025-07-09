import streamlit as st 
import traceback
from dotenv import load_dotenv
import os
import re
from utils import generate_resume, generate_cover_letter, convert_to_pdf

try:
    load_dotenv()
    st.set_page_config(page_title="AI Resume & Cover Letter Generator", layout="centered")

    st.title("🧠 AI Resume & Cover Letter Generator")
    st.subheader("Fill in your details below:")

    def is_valid_email(email):
        return re.match(r"[^@]+@[^@]+\.[^@]+", email)

    def is_valid_phone(phone):
        return re.match(r"^\d{10}$", phone)

    def is_valid_linkedin(link):
        return link == "" or re.match(r"^https?://(www\.)?linkedin\.com/.*", link)

    with st.form("resume_form"):
    # Section 1 - Personal & Job Info
        st.markdown("### 👤 Personal & Job Details")

        col1, col2 = st.columns(2)
        with col1:
          full_name = st.text_input("Full Name *", placeholder="Enter your full name")
          email = st.text_input("Email *", placeholder="example@gmail.com")
          phone = st.text_input("Phone Number *", placeholder="10-digit mobile number")
        with col2:
          job_title = st.text_input("Job Title You're Applying For *", placeholder="e.g., Data Analyst")
          company = st.text_input("Company Name *", placeholder="e.g., Accenture")

        st.markdown("---")  # Divider

    # Section 2 - Experience & Skills
        st.markdown("### 🧠 Experience & Skills")

        experience = st.text_area(" Work Experience / Projects *", placeholder="Mention key roles or projects")
        skills = st.text_area("Skills * (comma-separated)", placeholder="e.g., Python, SQL, Power BI")
        education = st.text_area("Education Background *", placeholder="Your degree, university, etc.")
        linkedin_url = st.text_input("🔗 LinkedIn Profile (Optional)", placeholder="LinkedIn URL")

        submit = st.form_submit_button("🚀 Generate Resume & Cover Letter")


    if submit:
        # === Validation ===
        errors = []
        if not full_name.strip():
            errors.append("Full Name is required.")
        if not email.strip() or not is_valid_email(email):
            errors.append("Valid Email is required.")
        if not phone.strip() or not is_valid_phone(phone):
            errors.append("Phone Number must be 10 digits.")
        if not job_title.strip():
            errors.append("Job Title is required.")
        if not company.strip():
            errors.append("Company Name is required.")
        if not experience.strip():
            errors.append("Experience is required.")
        if not skills.strip():
            errors.append("Skills are required.")
        if not education.strip():
            errors.append("Education Background is required.")
        if linkedin_url.strip() and not is_valid_linkedin(linkedin_url.strip()):
            errors.append("LinkedIn URL must start with https://linkedin.com/...")

        if errors:
            st.error("⚠️ Please fix the following issues before generating:")
            for err in errors:
                st.write(f"- {err}")
        else:
            with st.spinner("Generating documents..."):
                resume = generate_resume(full_name, email, phone, job_title, company, experience, skills, education, linkedin_url)
                cover_letter = generate_cover_letter(full_name, email, phone, job_title, company, experience, skills, education)

            st.subheader("📄 Resume")
            st.text_area("Generated Resume", resume, height=400)

            st.subheader("📄 Cover Letter")
            st.text_area("Generated Cover Letter", cover_letter, height=400)

            col1, col2 = st.columns(2)
            with col1:
                st.download_button("📥 Download Resume PDF", data=convert_to_pdf(resume), file_name="resume.pdf", mime="application/pdf")
            with col2:
                st.download_button("📥 Download Cover Letter PDF", data=convert_to_pdf(cover_letter), file_name="cover_letter.pdf", mime="application/pdf")

except Exception as e:
    st.error("An error occurred:")
    st.code(traceback.format_exc())
