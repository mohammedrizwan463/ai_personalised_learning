"""
app.py
------
AI Personalized Learning Assistant (Local LLaMA-3 Version)

Responsibilities:
- Run diagnostic quiz
- Analyze skill gaps
- Persist learning history
- Show learning trends
- Generate AI-driven learning roadmap (local LLaMA-3)
- Provide AI explanations & diagnostics
- Fully offline, no API keys, no quotas
"""

import streamlit as st

# =========================
# IMPORT PROJECT MODULES
# =========================
from quiz import run_quiz
from skill_gap import analyze_skill_gaps, get_weak_topics
from recommender import generate_learning_path, generate_recommendation_summary
from tutor import (
    get_ai_explanation,
    generate_learning_roadmap,
    explain_skill_gap
)
from profiler import (
    update_profile,
    load_profile,
    get_learning_trends
)

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="AI Personalized Learning Assistant",
    layout="wide"
)

st.title("🎓 AI-Powered Personalized Learning Assistant")
st.markdown(
    """
    This system uses a **locally hosted LLaMA-3 model** to diagnose learning gaps,
    explain concepts, and generate personalized learning roadmaps.
    
    ✔ Fully offline  
    ✔ No API keys  
    ✔ No usage limits  
    """
)

st.divider()

# =========================
# QUIZ FLOW
# =========================
quiz_done, scores = run_quiz()

if not quiz_done:
    st.info("Complete the diagnostic quiz to unlock personalized learning.")
    st.stop()

# =========================
# SKILL GAP ANALYSIS
# =========================
st.header("📊 Skill Gap Analysis")

skill_profile = analyze_skill_gaps(scores)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Topic Scores")
    for topic, data in skill_profile.items():
        st.write(f"{topic}: {data['score']}%")

with col2:
    st.subheader("Skill Levels")
    for topic, data in skill_profile.items():
        st.write(f"{topic}: {data['level']}")

st.divider()

# =========================
# PROFILE UPDATE & TRENDS
# =========================
update_profile(scores, skill_profile)
profile = load_profile()
learning_trends = get_learning_trends(profile)

# =========================
# LEARNING TRENDS
# =========================
st.header("📈 Learning Trends (Interactive)")

for topic, trend in learning_trends.items():
    if topic not in skill_profile:
        continue   # skip topics not in this quiz

    score = skill_profile[topic]["score"]
    level = skill_profile[topic]["level"]


    # Progress bar
    st.subheader(topic)
    st.progress(int(score))

    # Friendly status
    if trend == "Improving":
        status = "🟢 Improving"
        tip = "Keep going! Try slightly harder problems."
    elif trend == "Declining":
        status = "🔴 Declining"
        tip = "Revise basics and watch concept videos."
    else:
        status = "🟡 Stagnant"
        tip = "Practice daily for 20 minutes."

    st.write(f"**Status:** {status}")
    st.write(f"**Your level:** {level}")
    st.info(f"💡 Tip: {tip}")

    # Interactive button
    if st.button(f"Get AI advice for {topic}", key=f"trend_{topic}"):
        with st.spinner("AI analyzing your learning pattern..."):
            advice = get_ai_explanation(topic, level)
            st.success(advice)

    st.divider()


# =========================
# AI DIAGNOSTIC (WHY STUDENT IS WEAK)
# =========================
st.header("🧠 AI Diagnosis: Why These Gaps Exist")

weak_topics = get_weak_topics(skill_profile)

if weak_topics:
    selected_topic = st.selectbox(
        "Select a topic to understand why you are weak:",
        weak_topics
    )

    if st.button("Explain My Weakness"):
        with st.spinner("AI is analyzing your learning gaps..."):
            explanation = explain_skill_gap(
                topic=selected_topic,
                score=skill_profile[selected_topic]["score"],
                level=skill_profile[selected_topic]["level"]
            )
            st.write(explanation)
else:
    st.success("🎉 No weak topics detected. You are doing great!")

st.divider()

# =========================
# RULE-BASED LEARNING PATH
# =========================
st.header("🧩 System-Generated Learning Path")

learning_path = generate_learning_path(skill_profile)

for step in learning_path:
    st.write(
        f"➡️ **{step['action']}** — {step['topic']} "
        f"(_{step['reason']}_)"
    )

st.divider()

# =========================
# AI LEARNING ROADMAP (DAY-WISE)
# =========================
st.header("🗺️ Personalized AI Learning Roadmap")

if st.button("Generate My Learning Roadmap"):
    with st.spinner("AI is creating a personalized study plan..."):
        roadmap = generate_learning_roadmap(
            skill_profile={
                "skills": skill_profile,
                "trends": learning_trends,
                "attempts": profile["quiz_attempts"]
            }
        )
        st.write(roadmap)

st.divider()

# =========================
# AI TUTOR
# =========================
st.header("🤖 AI Learning Tutor")

if weak_topics:
    tutor_topic = st.selectbox(
        "Select a topic you want help with:",
        weak_topics,
        key="tutor_topic"
    )

    if st.button("Ask AI Tutor"):
        with st.spinner("AI Tutor is explaining the topic..."):
            explanation = get_ai_explanation(
                topic=tutor_topic,
                level=skill_profile[tutor_topic]["level"]
            )
            st.write(explanation)

st.divider()

# =========================
# SUMMARY
# =========================
st.header("📌 Learning Summary")

summary_text = generate_recommendation_summary(skill_profile)
st.success(summary_text)

st.divider()

# =========================
# RESET
# =========================

if st.button("Restart Learning Session"):
    st.session_state.clear()
    st.rerun()
