AI Personalised Learning

An AI-driven adaptive learning system that continuously analyzes student performance, learning trends, and behavioral patterns to dynamically personalize content, learning paths, and interventions.

--> Overview

AI Personalised Learning is a Python-based educational platform designed to provide tailored learning experiences for each learner. The system uses data from student interactions — including assessment scores, quiz results, skill gaps, and engagement trends — to generate intelligent recommendations, customized learning paths, and targeted interventions that evolve with user performance.

This repository implements the core components of an adaptive learning engine, including profiling, content recommendation, quiz generation, and performance analysis.

--> Key Features

✔ Dynamic Personalisation — Continuously adapts learning content and pacing based on individual student performance.
✔ Content Recommendation Engine — Suggests the most relevant learning materials based on skill gaps identified from data analysis.
✔ Skill Gap Detection — Identifies areas where learners require reinforcement or review.
✔ Interactive Quizzes — Generates custom quizzes to assess knowledge retention and guide future learning paths.
✔ Behavioral Analysis — Uses learner interaction patterns to better tailor engagement and pacing.

Note: You can extend these features by integrating AI/ML models for knowledge tracing, reinforcement learning, or NLP-driven content generation.

--> Project Structure
ai_personalised_learning/
├── data/                # Dataset files (e.g., student profiles, content metadata)
├── __pycache__/         # Cache directory
├── app.py               # Main application entry point
├── profiler.py          # Learner profile & analysis logic
├── quiz.py              # Quiz engine implementation
├── recommender.py       # Recommendation engine
├── skill_gap.py         # Skill gap detection logic
├── tutor.py             # Adaptive tutoring utilities
└── README.md            # Project documentation

--> Quick Start
--> Requirements

Python 3.8+

pip / venv or conda

--> Installation
# Clone the repository
git clone https://github.com/mohammedrizwan463/ai_personalised_learning.git
cd ai_personalised_learning

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt


--> If you don’t yet have requirements.txt, generate it with the packages you use (e.g., Flask, numpy, pandas, scikit-learn).

--> Usage
--> Run the Main App
python app.py


This launches the core application, which loads the learner data and starts the adaptive learning engine.

--> Recommendation API Example
from recommender import Recommender

rec = Recommender()
student_id = "user_001"
recommended_content = rec.get_recommendations(student_id)

print("Recommended Content:", recommended_content)

--> Running a Quiz
python quiz.py --student-id user_001

--> Example Output
Metric	Description
Skill Gap	Concepts where the learner shows weakness
Recommendations	Suggested learning modules or materials
Quiz Score	Performance on generated quizzes
Engagement Trends	Patterns analysis for pacing
--> Contributing

Contributions are welcome! To contribute:

Fork the repo

Create a new feature branch

Add tests & documentation

Submit a pull request

Please ensure the code follows consistent style and includes relevant test coverage.

--> License

This project is open source and available under the MIT License.

--> Acknowledgements

Thanks to open-source education and AI communities for inspiration in adaptive learning systems.
