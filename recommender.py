"""
recommender.py
--------------
Generates personalized learning recommendations and adaptive learning paths
based on identified skill gaps.

Input:
- skill_profile from skill_gap.py

Output:
- Ordered learning path
- Topic-wise recommendations with reasons
"""

from typing import Dict, List


# =========================
# CONFIG: DEFAULT TOPIC FLOW
# =========================
# This represents prerequisite order
DEFAULT_TOPIC_SEQUENCE = [
    "Basics",
    "Loops",
    "Functions"
]


# =========================
# CORE LOGIC
# =========================
def generate_learning_path(skill_profile: Dict[str, Dict]) -> List[Dict]:
    """
    Generate an adaptive learning path based on skill gaps.

    Args:
        skill_profile (dict):
            Output of analyze_skill_gaps(), example:
            {
                "Basics": {"score": 80, "level": "Strong", "needs_attention": False},
                "Loops": {"score": 40, "level": "Weak", "needs_attention": True}
            }

    Returns:
        list of dict:
            [
                {
                    "topic": "Loops",
                    "action": "Revise",
                    "reason": "Weak understanding detected"
                }
            ]
    """
    learning_path = []

    for topic in DEFAULT_TOPIC_SEQUENCE:
        if topic not in skill_profile:
            continue

        level = skill_profile[topic]["level"]

        if level == "Weak":
            learning_path.extend([
                {
                    "topic": topic,
                    "action": "Revise fundamentals",
                    "reason": "Low quiz performance"
                },
                {
                    "topic": topic,
                    "action": "Practice basic problems",
                    "reason": "Strengthen core understanding"
                },
                {
                    "topic": topic,
                    "action": "Re-attempt assessment",
                    "reason": "Validate improvement"
                }
            ])

        elif level == "Medium":
            learning_path.append({
                "topic": topic,
                "action": "Practice intermediate problems",
                "reason": "Partial understanding detected"
            })

        else:  # Strong
            learning_path.append({
                "topic": topic,
                "action": "Proceed to next topic",
                "reason": "Strong understanding confirmed"
            })

    return learning_path


# =========================
# TOPIC-SPECIFIC RECOMMENDATIONS
# =========================
def recommend_resources(skill_profile: Dict[str, Dict]) -> Dict[str, Dict]:
    """
    Generate resource recommendations per topic.

    Returns:
        dict:
            {
                "Loops": {
                    "recommended_level": "Beginner",
                    "focus": "Concept clarity"
                }
            }
    """
    recommendations = {}

    for topic, data in skill_profile.items():
        level = data["level"]

        if level == "Weak":
            recommendations[topic] = {
                "recommended_level": "Beginner",
                "focus": "Concept clarity and examples"
            }
        elif level == "Medium":
            recommendations[topic] = {
                "recommended_level": "Intermediate",
                "focus": "Practice and problem-solving"
            }
        else:
            recommendations[topic] = {
                "recommended_level": "Advanced",
                "focus": "Application and optimization"
            }

    return recommendations


# =========================
# SUMMARY (FOR DASHBOARD)
# =========================
def generate_recommendation_summary(skill_profile: dict) -> str:
    weak = []
    strong = []

    for topic, data in skill_profile.items():
        if data["level"] == "Weak":
            weak.append(topic)
        elif data["level"] == "Strong":
            strong.append(topic)

    summary = []

    if weak:
        summary.append(
            f"Immediate focus needed on {', '.join(weak)} due to weak conceptual clarity."
        )

    if strong:
        summary.append(
            f"You show strong understanding in {', '.join(strong)}. These can be leveraged to learn advanced topics faster."
        )

    summary.append(
        "Follow the AI roadmap consistently and revise weak topics with hands-on practice."
    )

    return " ".join(summary)
def explain_recommendation(topic, level, trend):
    return f"""
This recommendation was generated because:
- Topic: {topic}
- Skill level: {level}
- Learning trend: {trend}
"""
