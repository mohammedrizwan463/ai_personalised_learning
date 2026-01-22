"""
profiler.py
-----------
Manages student learning profile.

Responsibilities:
- Create student profile if not exists
- Update quiz scores
- Update skill-gap analysis
- Persist data to data/student_profile.json
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict


# =========================
# FILE PATHS
# =========================
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
PROFILE_FILE = DATA_DIR / "student_profile.json"


# =========================
# CORE FUNCTIONS
# =========================
def load_profile() -> Dict:
    """
    Load student profile from JSON file.
    If file does not exist, create a new profile structure.

    Returns:
        dict: student profile
    """
    if not PROFILE_FILE.exists():
        return _create_empty_profile()

    try:
        with open(PROFILE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        # If file is corrupted, reset safely
        return _create_empty_profile()


def save_profile(profile: Dict) -> None:
    """
    Save student profile to JSON file.
    """
    DATA_DIR.mkdir(exist_ok=True)

    with open(PROFILE_FILE, "w", encoding="utf-8") as f:
        json.dump(profile, f, indent=4)


def update_profile(
    scores: Dict[str, float],
    skill_profile: Dict[str, Dict]
) -> Dict:
    """
    Update student profile with latest quiz results and skill gaps.

    Args:
        scores (dict): topic-wise quiz scores
        skill_profile (dict): output of analyze_skill_gaps()

    Returns:
        dict: updated profile
    """
    profile = load_profile()

    timestamp = datetime.utcnow().isoformat()

    profile["last_updated"] = timestamp
    profile["quiz_attempts"] += 1

    # Update per-topic history
    for topic, score in scores.items():
        if topic not in profile["topics"]:
            profile["topics"][topic] = {
                "history": [],
                "current_score": None,
                "current_level": None
            }

        profile["topics"][topic]["history"].append({
            "score": round(score, 2),
            "level": skill_profile[topic]["level"],
            "timestamp": timestamp
        })

        profile["topics"][topic]["current_score"] = round(score, 2)
        profile["topics"][topic]["current_level"] = skill_profile[topic]["level"]

    save_profile(profile)
    return profile


# =========================
# PROFILE INITIALIZATION
# =========================
def _create_empty_profile() -> Dict:
    """
    Create a fresh student profile structure.
    """
    return {
        "student_id": "demo_student",
        "created_at": datetime.utcnow().isoformat(),
        "last_updated": None,
        "quiz_attempts": 0,
        "topics": {}
    }

def get_learning_trends(profile: dict) -> dict:
    """
    Analyze improvement or stagnation per topic.
    """
    trends = {}

    for topic, data in profile["topics"].items():
        history = data["history"]

        if len(history) < 2:
            trends[topic] = "Not enough data"
        else:
            diff = history[-1]["score"] - history[-2]["score"]
            if diff > 5:
                trends[topic] = "Improving"
            elif diff < -5:
                trends[topic] = "Declining"
            else:
                trends[topic] = "Stagnant"

    return trends

def analyze_learning_behavior(profile: dict) -> dict:
    behavior = {}

    for topic, data in profile["topics"].items():
        history = data["history"]

        if len(history) < 3:
            behavior[topic] = "Insufficient data"
            continue

        scores = [h["score"] for h in history]

        improvement_rate = (scores[-1] - scores[0]) / len(scores)

        if improvement_rate > 5:
            behavior[topic] = "Fast learner"
        elif improvement_rate > 0:
            behavior[topic] = "Slow but improving"
        else:
            behavior[topic] = "Needs intervention"

    return behavior
