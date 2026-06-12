import requests

APP_ID = "fd954513"
APP_KEY = "3b1f92349814751cb707e6fadca6d12a"

queries = [
    "Werkstudent Software",
    "Werkstudent Python",
    "Werkstudent Data",
    "Machine Learning",
    "Data Science",
    "KI Werkstudent"
]

for query in queries:
    url = "https://api.adzuna.com/v1/api/jobs/de/search/1"

    params = {
        "app_id": APP_ID,
        "app_key": APP_KEY,
        "what": query,
        "results_per_page": 3,
        "content-type": "application/json"
    }

    response = requests.get(url, params=params)
    data = response.json()

    print("\nQUERY:", query)
    print("STATUS:", response.status_code)
    print("COUNT:", data.get("count"))

    for job in data.get("results", []):
        print("-", job.get("title"))