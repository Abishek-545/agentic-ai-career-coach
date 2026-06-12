# 🤖 Agentic AI Career Coach

An end-to-end Multi-Agent AI application that helps students and job seekers find relevant jobs, evaluate resume-job fit, identify skill gaps, generate application materials, and practice interviews.

## Features

### Resume Analyzer Agent

* Extracts information from uploaded PDF resumes
* Identifies skills, projects, experience, and strengths
* Generates structured candidate profiles

### Job Search Agent

* Searches jobs using Adzuna API
* Supports custom roles and locations
* Filters and ranks relevant jobs

### ATS & Job Matching Agent

* Calculates ATS compatibility scores
* Evaluates skill match and experience match
* Provides job relevance insights

### Skill Gap Agent

* Identifies missing skills
* Suggests technologies to learn
* Recommends projects and certifications

### Application Assistant Agent

* Generates tailored application content
* Creates job-specific resume improvement suggestions
* Helps prepare application packages

### Mock Interview Agent

* Generates personalized interview questions
* Evaluates candidate answers
* Provides improvement recommendations

## Tech Stack

* Python
* Streamlit
* Google Gemini API
* Adzuna Job Search API
* Pandas
* PyPDF
* Multi-Agent Architecture

## Project Architecture

```text
Resume Upload
      ↓
Resume Analyzer Agent
      ↓
Job Search Agent
      ↓
Job Matching Agent
      ↓
Skill Gap Agent
      ↓
Application Assistant Agent
      ↓
Mock Interview Agent
```

## Installation

Clone the repository:

```bash
git clone https://github.com/Abishek-545/agentic-ai-career-coach.git
cd agentic-ai-career-coach
```

Create virtual environment:

```bash
python -m venv venv
```

Activate environment:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create `.env` file:

```env
GEMINI_API_KEY=your_gemini_key

ADZUNA_APP_ID=your_adzuna_app_id
ADZUNA_APP_KEY=your_adzuna_app_key
```

Run:

```bash
streamlit run app.py
```

## Future Enhancements

* Automated job application agent
* LinkedIn profile analysis
* Resume optimization engine
* Application tracking dashboard
* Multi-model LLM support
* Docker deployment
* Cloud deployment (AWS/Azure/GCP)

## Author

Abishek Thirupathi

GitHub:
https://github.com/Abishek-545
