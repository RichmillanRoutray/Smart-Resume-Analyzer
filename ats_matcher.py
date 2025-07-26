import re
from collections import Counter

# Define actual useful keywords
SKILL_KEYWORDS = [
    "python", "java", "sql", "javascript", "html", "css", "c++", "c#", "nodejs",
    "react", "angular", "pandas", "numpy", "matplotlib", "excel", "tableau",
    "machine learning", "deep learning", "data science", "data analysis",
    "nlp", "aws", "azure", "gcp", "git", "docker", "kubernetes", "linux", "django", "flask"
]

def extract_keywords(text):
    text = text.lower()
    found_keywords = []
    for keyword in SKILL_KEYWORDS:
        if re.search(rf"\b{re.escape(keyword)}\b", text):
            found_keywords.append(keyword)
    return found_keywords

def get_keyword_overlap(resume_text, jd_text):
    resume_keywords = extract_keywords(resume_text)
    jd_keywords = extract_keywords(jd_text)

    resume_counter = Counter(resume_keywords)
    jd_counter = Counter(jd_keywords)

    matched = set(resume_keywords) & set(jd_keywords)
    unique_jd_keywords = set(jd_keywords)
    coverage = len(matched) / len(unique_jd_keywords) * 100 if unique_jd_keywords else 0

    return {
        "matched_keywords": sorted(list(matched)),
        "coverage_percent": round(coverage, 2),
        "top_resume_keywords": resume_counter.most_common(10),
        "top_jd_keywords": jd_counter.most_common(10)
    }
