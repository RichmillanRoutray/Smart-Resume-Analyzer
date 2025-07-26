import fitz
from pydantic import BaseModel
import re

class ResumeData(BaseModel):
    name: str = ""
    skills: list[str] = []
    experience: str = ""

class JobData(BaseModel):
    title: str = ""
    skills_required: list[str] = []
    experience_required: str = ""

def extract_text_from_pdf(uploaded_file):
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text.strip()

# Extract skills using common keywords
def extract_skills(text):
    # Customize this list or load dynamically from a skills DB
    common_skills = [
        "python", "java", "c++", "sql", "javascript", "html", "css", "machine learning",
        "data analysis", "excel", "pandas", "numpy", "deep learning", "flask", "django",
        "react", "nodejs", "cloud", "aws", "azure", "git", "linux"
    ]
    found = set()
    for skill in common_skills:
        if re.search(rf"\b{re.escape(skill)}\b", text, re.IGNORECASE):
            found.add(skill.lower())
    return list(found)

def extract_experience(text):
    # Rough pattern to match something like "2 years", "5+ years", etc.
    match = re.search(r'(\d+)\s*\+?\s*years?', text.lower())
    return match.group(0) if match else "Not specified"

def parse_resume(text):
    skills = extract_skills(text)
    experience = extract_experience(text)
    return ResumeData(name="", skills=skills, experience=experience)

def parse_job_description(text):
    skills_required = extract_skills(text)
    experience_required = extract_experience(text)
    title_match = re.search(r'(title|position)[:\-]?\s*(.+)', text.lower())
    title = title_match.group(2).strip().capitalize() if title_match else "Unknown"
    return JobData(title=title, skills_required=skills_required, experience_required=experience_required)
