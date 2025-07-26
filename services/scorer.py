def score_match(resume, job):
    matched_skills = list(set(resume.skills) & set(job.skills_required))
    score = int((len(matched_skills) / len(job.skills_required)) * 100) if job.skills_required else 0
    return {
        "match_score": score,
        "matched_skills": matched_skills,
        "missing_skills": list(set(job.skills_required) - set(resume.skills))
    }