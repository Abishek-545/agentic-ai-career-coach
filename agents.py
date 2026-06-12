from config import get_gemini_client, GEMINI_MODEL
from utils import extract_json

client = get_gemini_client()


def ask_gemini(prompt):
    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt
    )
    return response.text


def resume_analyzer_agent(resume_text):
    prompt = f"""
You are Resume Analyzer Agent.

Analyze this resume and return JSON only.

Resume:
{resume_text}

Return:
{{
  "profile_summary": "",
  "technical_skills": [],
  "soft_skills": [],
  "projects": [],
  "experience": [],
  "education": [],
  "strengths": [],
  "weaknesses": [],
  "best_fit_roles": []
}}
"""
    return extract_json(ask_gemini(prompt))


def job_relevance_agent(resume_text, target_role, job):
    prompt = f"""
You are Job Relevance Agent.

Your task is to decide whether this job is relevant to the candidate and target role.

Candidate resume:
{resume_text}

Target role:
{target_role}

Job:
Title: {job["title"]}
Company: {job["company"]}
Location: {job["location"]}
Description: {job["description"]}

Return JSON only:
{{
  "is_relevant": true,
  "relevance_score": 0,
  "reason": "",
  "job_type": "",
  "role_category": "",
  "seniority_level": "",
  "red_flags": []
}}

Rules:
- relevance_score must be 0 to 100.
- If target role is "AI ML Werkstudent", prefer AI, ML, data science, NLP, computer vision, Python, software, or research student roles.
- If target role is custom, judge based on that custom role.
- Penalize unrelated marketing, sales, recruiter, construction, project manager, and senior leadership jobs unless the target role asks for them.
- For Werkstudent target roles, prefer working student, intern, student assistant, thesis, junior, or entry-level roles.
"""
    return extract_json(ask_gemini(prompt))


def job_matching_agent(resume_text, job):
    prompt = f"""
You are Job Matching Agent.

Compare the resume with this job and return JSON only.

Resume:
{resume_text}

Job Title:
{job["title"]}

Company:
{job["company"]}

Job Description:
{job["description"]}

Return:
{{
  "ats_score": 0,
  "skill_match": 0,
  "experience_match": 0,
  "placement_chance": "",
  "match_level": "",
  "matched_skills": [],
  "missing_skills": [],
  "missing_keywords": [],
  "reason": ""
}}

Scores must be from 0 to 100.
placement_chance must be Low, Medium, Good, or High.
match_level must be Low Fit, Medium Fit, Good Fit, or Strong Fit.
"""
    return extract_json(ask_gemini(prompt))


def skill_gap_agent(resume_text, job):
    prompt = f"""
You are Skill Gap Agent.

Find skill gaps for this job.

Resume:
{resume_text}

Job Description:
{job["description"]}

Return JSON only:
{{
  "top_missing_skills": [],
  "skills_to_learn_first": [],
  "mini_projects_to_build": [],
  "resume_improvement_suggestions": [],
  "learning_roadmap_30_days": []
}}
"""
    return extract_json(ask_gemini(prompt))


def application_assistant_agent(resume_text, job):
    prompt = f"""
You are Application Assistant Agent.

Create a tailored application package.

Resume:
{resume_text}

Job:
{job}

Return:
1. Short cover letter
2. LinkedIn recruiter message
3. Email message
4. Resume bullet improvements
5. Application checklist

Do not claim experience that is not in the resume.
"""
    return ask_gemini(prompt)


def mock_interview_agent(resume_text, job, num_questions):
    prompt = f"""
You are Mock Interview Agent.

Generate exactly {num_questions} interview questions for this job.

Resume:
{resume_text}

Job Description:
{job["description"]}

Include:
- technical questions
- project questions
- behavioral questions
- role-specific scenario questions

Return only numbered questions.
"""
    return ask_gemini(prompt)


def evaluate_interview_answer(question, answer, job):
    prompt = f"""
You are Interview Evaluation Agent.

Job:
{job["title"]}

Question:
{question}

Candidate Answer:
{answer}

Evaluate answer.

Return:
Overall Score: /10
Technical Accuracy: /10
Communication: /10
Job Relevance: /10

Strengths:
-

Weaknesses:
-

Improved Answer:
-

Interview Tip:
-
"""
    return ask_gemini(prompt)