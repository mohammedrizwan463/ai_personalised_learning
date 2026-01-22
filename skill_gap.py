"""
skill_gap.py
------------
Handles skill gap analysis based on quiz scores.

Responsibilities:
- Classify student skill levels per topic
- Generate interpretable skill-gap summary
- Provide clean API for app.py and recommender.py
"""

from typing import Dict


# =========================
# CONFIGURABLE THRESHOLDS
# =========================
WEAK_THRESHOLD = 50
MEDIUM_THRESHOLD = 75


# =========================
# CORE LOGIC
# =========================
def classify_skill(score: float) -> str:
    """
    Classify skill level based on score.

    Args:
        score (float): Percentage score (0–100)

    Returns:
        str: 'Weak', 'Medium', or 'Strong'
    """
    if score < WEAK_THRESHOLD:
        return "Weak"
    elif score < MEDIUM_THRESHOLD:
        return "Medium"
    else:
        return "Strong"


def analyze_skill_gaps(scores: Dict[str, float]) -> Dict[str, Dict]:
    """
    Analyze topic-wise scores and identify skill gaps.

    Args:
        scores (dict):
            {
                "Basics": 80,
                "Loops": 40,
                "Functions": 65
            }

    Returns:
        dict:
            {
                "Basics": {
                    "score": 80,
                    "level": "Strong",
                    "needs_attention": False
                },
                "Loops": {
                    "score": 40,
                    "level": "Weak",
                    "needs_attention": True
                }
            }
    """
    skill_profile = {}

    for topic, score in scores.items():
        level = classify_skill(score)

        skill_profile[topic] = {
            "score": round(score, 2),
            "level": level,
            "needs_attention": level == "Weak"
        }

    return skill_profile


# =========================
# UTILITY FUNCTIONS
# =========================
def get_weak_topics(skill_profile: Dict[str, Dict]) -> list:
    """
    Extract list of weak topics.

    Args:
        skill_profile (dict): Output of analyze_skill_gaps()

    Returns:
        list: Topics where skill level is 'Weak'
    """
    return [
        topic
        for topic, data in skill_profile.items()
        if data["level"] == "Weak"
    ]


def get_skill_summary(skill_profile: Dict[str, Dict]) -> Dict[str, int]:
    """
    Generate a summary count of skill levels.

    Returns:
        dict:
            {
                "Weak": 1,
                "Medium": 1,
                "Strong": 1
            }
    """
    summary = {"Weak": 0, "Medium": 0, "Strong": 0}

    for data in skill_profile.values():
        summary[data["level"]] += 1

    return summary
