"""
quiz.py
-------
Handles diagnostic quiz logic.
- Loads questions from data/questions.csv
- Renders quiz using Streamlit
- Evaluates answers
- Returns topic-wise scores
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import random


# =========================
# FILE PATHS
# =========================
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
QUESTIONS_FILE = DATA_DIR / "questions.csv"

# =========================
# LOAD QUESTIONS
# =========================
def load_questions():
    df = pd.read_csv(QUESTIONS_FILE)

    easy = df[df["difficulty"]=="Easy"]
    medium = df[df["difficulty"]=="Medium"]
    hard = df[df["difficulty"]=="Hard"]

    selected = []

    if len(easy) >= 3:
        selected.append(easy.sample(3))
    if len(medium) >= 4:
        selected.append(medium.sample(4))
    if len(hard) >= 3:
        selected.append(hard.sample(3))

    df_final = pd.concat(selected)

    if len(df_final) == 10:
        df_final = df.sample(10)

    return df_final.sample(frac=1).reset_index(drop=True)




# =========================
# SESSION STATE INIT
# =========================
def init_quiz_state():
    if "quiz_answers" not in st.session_state:
        st.session_state.quiz_answers = {}

    if "quiz_submitted" not in st.session_state:
        st.session_state.quiz_submitted = False

def filter_questions(df, level):
    if level == "Weak":
        return df[df["difficulty"].isin(["Easy", "Medium"])]
    elif level == "Medium":
        return df[df["difficulty"].isin(["Medium", "Hard"])]
    else:
        return df

# =========================
# RENDER QUIZ
# =========================
def render_quiz(df):
    st.header("📋 Diagnostic Quiz")

    for _, row in df.iterrows():
        q_id = int(row["id"])
        options = [
            row["option1"],
            row["option2"],
            row["option3"],
            row["option4"]
        ]

        st.subheader(row["question"])

        selected = st.radio(
            "Choose one option:",
            options,
            key=f"question_{q_id}"
        )

        st.session_state.quiz_answers[q_id] = selected

    # ✅ FIX: submit button INSIDE function
    if st.button("Submit Quiz"):
        st.session_state.quiz_submitted = True
        st.rerun()


# =========================
# EVALUATE QUIZ
# =========================
def evaluate_quiz(df):
    topic_stats = {}

    for _, row in df.iterrows():
        q_id = int(row["id"])
        topic = row["topic"]
        correct_answer = row["answer"]
        user_answer = st.session_state.quiz_answers.get(q_id)

        if topic not in topic_stats:
            topic_stats[topic] = {"correct": 0, "total": 0}

        if user_answer == correct_answer:
            topic_stats[topic]["correct"] += 1

        topic_stats[topic]["total"] += 1

    topic_scores = {}
    for topic, stats in topic_stats.items():
        topic_scores[topic] = (stats["correct"] / stats["total"]) * 100

    return topic_scores


# =========================
# PUBLIC API
# =========================
def run_quiz():
    init_quiz_state()

    # Generate questions only once
    if "quiz_df" not in st.session_state:
        st.session_state.quiz_df = load_questions()

    df = st.session_state.quiz_df

    from profiler import load_profile
    profile = load_profile()

    if profile["quiz_attempts"] > 0:
        avg_level = "Medium"
        df = filter_questions(df, avg_level)

    if not st.session_state.quiz_submitted:
        render_quiz(df)
        return False, None
    else:
        scores = evaluate_quiz(df)
        return True, scores
