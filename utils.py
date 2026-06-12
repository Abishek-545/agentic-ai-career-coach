import json
import re
from pypdf import PdfReader


def extract_pdf_text(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text.strip()


def extract_json(text):
    try:
        return json.loads(text)
    except Exception:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except Exception:
                return {}
        return {}


def parse_questions(text):
    questions = []

    for line in text.split("\n"):
        line = line.strip()
        match = re.match(r"^\d+[\.\)]\s*(.+)", line)

        if match:
            questions.append(match.group(1).strip())

    return questions


def build_interview_report(history):
    report = "Mock Interview Report\n\n"

    for i, item in enumerate(history, start=1):
        report += f"""
Question {i}:
{item["question"]}

Answer:
{item["answer"]}

Evaluation:
{item["evaluation"]}

-----------------------------
"""

    return report


def clean_html(text):
    return re.sub(r"<.*?>", " ", text or "").strip()