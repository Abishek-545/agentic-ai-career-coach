import pandas as pd
import streamlit as st

from utils import extract_pdf_text, parse_questions, build_interview_report
from job_search import search_adzuna_jobs
from agents import (
    resume_analyzer_agent,
    job_matching_agent,
    skill_gap_agent,
    application_assistant_agent,
    mock_interview_agent,
    evaluate_interview_answer
)


st.set_page_config(
    page_title="Agentic AI Career Coach",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Agentic AI Job Search & Career Coach")
st.write(
    "A quota-efficient multi-agent AI application that analyzes resumes, finds relevant jobs, "
    "calculates ATS scores, identifies skill gaps, prepares applications, and conducts mock interviews."
)




with st.sidebar:
    st.header("Settings")

    target_role = st.text_input("Target Role", value="AI ML Werkstudent")
    location = st.text_input("Location", value="Germany")

    max_jobs = st.slider("Number of Jobs to Show", 1, 10, 5)
    num_interview_questions = st.slider("Mock Interview Questions", 3, 10, 5)

    if st.button("Reset App"):
        st.session_state.clear()
        st.rerun()

current_search_key = f"{target_role}_{location}_{max_jobs}"

if "last_search_key" not in st.session_state:
    st.session_state["last_search_key"] = current_search_key

if st.session_state["last_search_key"] != current_search_key:
    keys_to_clear = [
        "jobs",
        "selected_analysis",
        "application_package",
        "interview_questions",
        "current_question",
        "interview_history"
    ]

    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]

    st.session_state["last_search_key"] = current_search_key

uploaded_resume = st.file_uploader("Upload Resume PDF", type=["pdf"])

if uploaded_resume:
    resume_text = extract_pdf_text(uploaded_resume)

    if len(resume_text) < 100:
        st.error("Could not extract enough text from resume.")
        st.stop()

    st.session_state["resume_text"] = resume_text
    st.success("Resume uploaded and extracted successfully.")

    with st.expander("Preview Resume Text"):
        st.write(resume_text[:3000])

    if st.button("Run Resume Analyzer Agent"):
        with st.spinner("Resume Analyzer Agent is working..."):
            st.session_state["resume_analysis"] = resume_analyzer_agent(resume_text)


if "resume_analysis" in st.session_state:
    st.subheader("🧠 Resume Analyzer Agent Output")
    st.json(st.session_state["resume_analysis"])


if "resume_text" in st.session_state:
    resume_text = st.session_state["resume_text"]

    st.divider()
    st.subheader("🔎 Job Search Agent")

    manual_job = st.text_area(
        "Optional: Paste a job description manually",
        height=180
    )

    col1, col2 = st.columns(2)

    with col1:
        search_clicked = st.button("Find Relevant Jobs")

    with col2:
        manual_clicked = st.button("Use Manual Job Description")

    if search_clicked:
        with st.spinner("Searching jobs from Adzuna..."):
            jobs = search_adzuna_jobs(
                target_role=target_role,
                location=location,
                max_jobs=max_jobs,
                results_per_query=10
            )

        if not jobs:
            st.warning(
                "No relevant jobs found. Try a broader role, different location, "
                "or paste a job description manually."
            )
        else:
            st.session_state["jobs"] = jobs
            st.success(f"Found {len(jobs)} relevant jobs.")

    if manual_clicked:
        if not manual_job.strip():
            st.warning("Please paste a job description.")
        else:
            st.session_state["jobs"] = [{
                "title": target_role,
                "company": "Manual Job Input",
                "location": location,
                "description": manual_job,
                "url": "N/A",
                "source": "Manual",
                "relevance_score": 100,
                "relevance_reason": "Manual job description provided by user.",
                "job_type": "Manual",
                "seniority_level": "Unknown"
            }]
            st.success("Manual job added.")


if "jobs" in st.session_state:
    st.subheader("📌 Jobs Found")

    for i, job in enumerate(st.session_state["jobs"]):
        with st.expander(
            f"{i + 1}. {job['title']} - {job['company']} | Relevance: {job.get('relevance_score', 0)}"
        ):
            st.write(f"**Location:** {job['location']}")
            st.write(f"**Source:** {job.get('source', 'Unknown')}")
            st.write(f"**URL:** {job['url']}")
            st.write(f"**Why relevant:** {job.get('relevance_reason', '')}")
            st.write(job["description"][:1500])

    selected_job_label = st.selectbox(
        "Select one job for AI analysis",
        [
            f"{i + 1}. {job['title']} - {job['company']}"
            for i, job in enumerate(st.session_state["jobs"])
        ]
    )

    selected_index = int(selected_job_label.split(".")[0]) - 1
    selected_job = st.session_state["jobs"][selected_index]

    if st.button("Run ATS + Skill Gap Agents for Selected Job"):
        with st.spinner("Job Matching Agent is analyzing selected job..."):
            match_result = job_matching_agent(
                st.session_state["resume_text"],
                selected_job
            )

        with st.spinner("Skill Gap Agent is analyzing selected job..."):
            gap_result = skill_gap_agent(
                st.session_state["resume_text"],
                selected_job
            )

        st.session_state["selected_analysis"] = {
            "job": selected_job,
            "match": match_result,
            "gap": gap_result
        }


if "selected_analysis" in st.session_state:
    st.divider()
    st.subheader("📊 Selected Job Analysis")

    job = st.session_state["selected_analysis"]["job"]
    match = st.session_state["selected_analysis"]["match"]
    gap = st.session_state["selected_analysis"]["gap"]

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("ATS Score", f"{match.get('ats_score', 0)}%")

    with col2:
        st.metric("Skill Match", f"{match.get('skill_match', 0)}%")

    with col3:
        st.metric("Experience Match", f"{match.get('experience_match', 0)}%")

    with col4:
        st.metric("Relevance", job.get("relevance_score", 0))

    st.subheader("✅ Match Details")
    st.json(match)

    st.subheader("📉 Skill Gap Agent Output")
    st.json(gap)

    st.divider()
    st.subheader("📝 Application Assistant Agent")

    if st.button("Generate Application Package"):
        with st.spinner("Application Assistant Agent is preparing your package..."):
            st.session_state["application_package"] = application_assistant_agent(
                st.session_state["resume_text"],
                job
            )

    if "application_package" in st.session_state:
        st.write(st.session_state["application_package"])

        st.download_button(
            "Download Application Package",
            st.session_state["application_package"],
            file_name="application_package.txt",
            mime="text/plain"
        )

    st.divider()
    st.subheader("🎤 Mock Interview Agent")

    if st.button("Generate Mock Interview"):
        with st.spinner("Mock Interview Agent is generating questions..."):
            questions_raw = mock_interview_agent(
                st.session_state["resume_text"],
                job,
                num_interview_questions
            )

        st.session_state["interview_questions"] = parse_questions(questions_raw)
        st.session_state["current_question"] = 0
        st.session_state["interview_history"] = []

    if "interview_questions" in st.session_state:
        questions = st.session_state["interview_questions"]

        if questions:
            current_index = st.session_state["current_question"]

            st.write(f"### Question {current_index + 1} of {len(questions)}")
            current_question = questions[current_index]
            st.info(current_question)

            answer = st.text_area(
                "Your Answer",
                key=f"answer_{current_index}",
                height=160
            )

            col1, col2 = st.columns(2)

            with col1:
                if st.button("Evaluate Answer"):
                    if not answer.strip():
                        st.warning("Please write your answer.")
                    else:
                        with st.spinner("Interview Evaluation Agent is evaluating..."):
                            evaluation = evaluate_interview_answer(
                                current_question,
                                answer,
                                job
                            )

                        st.session_state["interview_history"].append({
                            "question": current_question,
                            "answer": answer,
                            "evaluation": evaluation
                        })

                        st.write(evaluation)

            with col2:
                if st.button("Next Question"):
                    if current_index < len(questions) - 1:
                        st.session_state["current_question"] += 1
                        st.rerun()
                    else:
                        st.success("Mock interview completed.")

            if st.session_state.get("interview_history"):
                st.subheader("Interview History")

                for i, item in enumerate(
                    st.session_state["interview_history"],
                    start=1
                ):
                    with st.expander(f"Question {i} Review"):
                        st.write("**Question:**")
                        st.write(item["question"])

                        st.write("**Answer:**")
                        st.write(item["answer"])

                        st.write("**Evaluation:**")
                        st.write(item["evaluation"])

                report = build_interview_report(
                    st.session_state["interview_history"]
                )

                st.download_button(
                    "Download Interview Report",
                    report,
                    file_name="mock_interview_report.txt",
                    mime="text/plain"
                )