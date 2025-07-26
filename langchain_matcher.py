import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

load_dotenv()

def analyze_match_with_llm(resume_text, job_description_text):
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found in environment variables.")

    prompt = PromptTemplate.from_template("""
You are a professional HR assistant. Based on the resume and job description below, perform the following:
1. Identify candidate strengths.
2. List missing skills/requirements.
3. Estimate a match score (0-100).
4. Suggest improvements for the resume.

Resume:
{resume_text}

Job Description:
{job_description_text}
""")

    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.3,
        api_key=api_key
    )
    chain = LLMChain(llm=llm, prompt=prompt)

    return chain.run(resume_text=resume_text, job_description_text=job_description_text)
