def calculate_score(resume_text, job_description):

    resume_text = resume_text.lower()
    job_description = job_description.lower()

    resume_words = set(resume_text.split())
    job_words = set(job_description.split())

    match_words = resume_words.intersection(job_words)

    score = len(match_words) / len(job_words) * 100

    return round(score, 2)