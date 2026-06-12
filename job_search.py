import requests
import re
from config import get_adzuna_credentials
from utils import clean_html


COUNTRY_MAP = {
    "germany": "de",
    "deutschland": "de",
    "austria": "at",
    "uk": "gb",
    "united kingdom": "gb",
    "usa": "us",
    "united states": "us",
    "canada": "ca",
    "india": "in",
    "france": "fr"
}


def infer_country_code(location: str):
    location_lower = location.lower().strip()

    for key, value in COUNTRY_MAP.items():
        if key in location_lower:
            return value

    return "de"


def normalize(text):
    return re.sub(r"[^a-zA-Z0-9+# ]", " ", text.lower())


def build_search_queries(target_role: str):
    role = target_role.strip()
    role_lower = role.lower()

    queries = [role]

    if "frontend" in role_lower or "front end" in role_lower:
        queries.extend([
            "Frontend Werkstudent",
            "Frontend Working Student",
            "Frontend Internship",
            "React Werkstudent",
            "React Working Student",
            "JavaScript Werkstudent",
            "Angular Werkstudent"
        ])

    elif "backend" in role_lower:
        queries.extend([
            "Backend Werkstudent",
            "Backend Working Student",
            "Java Werkstudent",
            "Spring Boot Werkstudent",
            "Python Backend Werkstudent"
        ])

    elif "ai" in role_lower or "ml" in role_lower or "machine learning" in role_lower:
        queries.extend([
            "Machine Learning Werkstudent",
            "AI Werkstudent",
            "Data Science Werkstudent",
            "KI Werkstudent",
            "Python Werkstudent"
        ])

    elif "data" in role_lower:
        queries.extend([
            "Data Analyst Werkstudent",
            "Data Science Werkstudent",
            "Business Intelligence Werkstudent",
            "SQL Werkstudent"
        ])

    elif "devops" in role_lower or "cloud" in role_lower:
        queries.extend([
            "DevOps Werkstudent",
            "Cloud Werkstudent",
            "AWS Werkstudent",
            "Kubernetes Werkstudent"
        ])

    else:
        queries.extend([
            role.replace("internship", "intern"),
            role.replace("Werkstudent", "Working Student"),
            role.replace("Working Student", "Werkstudent")
        ])

    unique = []
    for q in queries:
        q = q.strip()
        if q and q not in unique:
            unique.append(q)

    return unique


def get_role_keywords(target_role):
    role = normalize(target_role)

    if "frontend" in role or "front end" in role:
        return [
            "frontend", "front end", "react", "angular", "vue",
            "javascript", "typescript", "html", "css", "web developer"
        ]

    if "backend" in role:
        return [
            "backend", "java", "spring", "spring boot",
            "python", "django", "flask", "api", "rest"
        ]

    if "ai" in role or "ml" in role or "machine learning" in role:
        return [
            "machine learning", "artificial intelligence", "ai", "ki",
            "data science", "python", "pytorch", "tensorflow",
            "computer vision", "nlp"
        ]

    if "data" in role:
        return [
            "data", "data science", "data analyst", "sql",
            "python", "power bi", "tableau", "analytics"
        ]

    if "devops" in role or "cloud" in role:
        return [
            "devops", "cloud", "aws", "azure", "docker",
            "kubernetes", "ci cd", "linux"
        ]

    return [
        word for word in role.split()
        if len(word) > 2 and word not in ["werkstudent", "internship", "intern"]
    ]


def keyword_relevance_score(job, target_role):
    text = normalize(f"{job['title']} {job['description']}")
    role_keywords = get_role_keywords(target_role)

    score = 0

    for keyword in role_keywords:
        if keyword in text:
            score += 35

    student_words = [
        "werkstudent",
        "working student",
        "intern",
        "internship",
        "praktikum",
        "student"
    ]

    for word in student_words:
        if word in text:
            score += 25

    bad_words = [
        "senior", "lead", "manager", "director", "head of",
        "recruiter", "sales", "marketing", "bauleiter",
        "projektleiter", "social media"
    ]

    target = normalize(target_role)

    if not any(x in target for x in ["senior", "manager", "lead", "marketing"]):
        for word in bad_words:
            if word in text:
                score -= 60

    return max(score, 0)


def search_adzuna_jobs(target_role, location, max_jobs=5, results_per_query=10):
    app_id, app_key = get_adzuna_credentials()

    if not app_id or not app_key:
        return []

    country = infer_country_code(location)
    queries = build_search_queries(target_role)

    all_jobs = []
    seen_urls = set()

    for query in queries:
        url = f"https://api.adzuna.com/v1/api/jobs/{country}/search/1"

        params = {
            "app_id": app_id,
            "app_key": app_key,
            "what": query,
            "results_per_page": results_per_query,
            "content-type": "application/json"
        }

        if location.lower() not in ["germany", "deutschland", "de"]:
            params["where"] = location

        try:
            response = requests.get(url, params=params, timeout=20)

            if response.status_code != 200:
                continue

            data = response.json().get("results", [])

            for item in data:
                job_url = item.get("redirect_url", "")

                if job_url in seen_urls:
                    continue

                seen_urls.add(job_url)

                company = item.get("company", {})
                location_data = item.get("location", {})

                job = {
                    "title": item.get("title", ""),
                    "company": company.get("display_name", "Unknown"),
                    "location": location_data.get("display_name", location),
                    "description": clean_html(item.get("description", ""))[:5000],
                    "url": job_url,
                    "source": "Adzuna",
                    "search_query": query
                }

                score = keyword_relevance_score(job, target_role)

                if score >= 50:
                    job["relevance_score"] = score
                    job["relevance_reason"] = f"Matched search query: {query}"
                    all_jobs.append(job)

        except Exception:
            continue

    all_jobs = sorted(
        all_jobs,
        key=lambda x: x.get("relevance_score", 0),
        reverse=True
    )

    return all_jobs[:max_jobs]