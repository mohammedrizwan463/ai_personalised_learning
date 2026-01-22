import os
os.environ["OLLAMA_NO_CUDA"] = "1"   # hard-disable GPU

import ollama

# Primary and fallback models
MODEL = "qwen2.5:3b"


# =========================
# CORE LLM CALL
# =========================
def call_llm(prompt: str) -> str:
    response = ollama.chat(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )
    return response["message"]["content"].strip()


# =========================
# PROMPT BUILDERS (UNCHANGED)
# =========================
def build_tutor_prompt(topic: str, level: str) -> str:
    return f"""
You are an expert programming tutor.

Topic: {topic}
Student level: {level}

Explain the topic clearly.

Include:
1. Definition (1–2 lines)
2. Brief explanation with example
3. Where it is used
4. YouTube search suggestions

Format:
Definition:
Explanation:
Usage:
YouTube searches:
"""


def build_roadmap_prompt(skill_profile: dict) -> str:
    return f"""
You are an adaptive learning AI.

Student data:
- Skill gaps
- Learning trends
- Learning speed patterns
- Quiz attempts

{skill_profile}

Generate a DAY-WISE adaptive learning plan.

Rules:
- Weak + slow learners → more revision
- Fast learners → compressed roadmap
- Declining topics → intervention focus
"""


def build_diagnosis_prompt(topic: str, score: float, level: str) -> str:
    return f"""
You are an educational diagnostician.

Topic: {topic}
Score: {score}%
Level: {level}

Explain:
- Why the student is weak
- Common mistakes
- How to improve
"""


# =========================
# PUBLIC FUNCTIONS (UNCHANGED)
# =========================
def get_ai_explanation(topic: str, level: str) -> str:
    return call_llm(build_tutor_prompt(topic, level))


def generate_learning_roadmap(skill_profile: dict) -> str:
    return call_llm(build_roadmap_prompt(skill_profile))


def explain_skill_gap(topic: str, score: float, level: str) -> str:
    return call_llm(build_diagnosis_prompt(topic, score, level))
