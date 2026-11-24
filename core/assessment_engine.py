from core.llm_engine import generate_json
from core.knowledge_gap import analyze_assessment

DEMO_QUESTIONS = {
    "Mathematics": [
        {"type":"multiple_choice","question":"What is 12 + 8?","options":["18","20","22","30"],"answer":"20","concept":"Addition"},
        {"type":"multiple_choice","question":"What is 7 x 6?","options":["36","40","42","48"],"answer":"42","concept":"Multiplication"},
        {"type":"short_answer","question":"In y = 2x + 3, find y when x = 4.","answer":"11","concept":"Linear equations"},
        {"type":"multiple_choice","question":"What is 25% of 80?","options":["15","20","25","30"],"answer":"20","concept":"Percentages"},
        {"type":"short_answer","question":"What is the perimeter of a square of side 5 units?","answer":"20","concept":"Perimeter"},
    ],
    "Computer Science": [
        {"type":"multiple_choice","question":"Which value represents true in binary?","options":["0","1","-1","10"],"answer":"1","concept":"Binary values"},
        {"type":"short_answer","question":"What does a variable store?","answer":"a value","concept":"Variables"},
        {"type":"multiple_choice","question":"Which structure repeats a block?","options":["Loop","Class","String","Index"],"answer":"Loop","concept":"Loops"},
        {"type":"short_answer","question":"What is a function?","answer":"reusable block","concept":"Functions"},
        {"type":"multiple_choice","question":"Which operator checks equality in Python?","options":["=","==","!=","+"],"answer":"==","concept":"Comparisons"},
    ],
}


def generate_diagnostic(subject, topic):
    data = generate_json(
        f"Create exactly five mixed diagnostic questions for {subject}: {topic}. "
        "Use three multiple_choice and two short_answer entries. Include question, type, options where applicable, "
        "answer, and concept. Return JSON with a 'questions' array.",
        "Generate a valid educational assessment. Return only JSON."
    )
    if data and isinstance(data.get("questions"), list):
        return data["questions"][:5]
    base = DEMO_QUESTIONS.get(subject)
    if base:
        return [{**q, "topic": topic} for q in base]
    return [{**q, "topic": topic} for q in DEMO_QUESTIONS["Mathematics"]]


def evaluate(questions, answers):
    return analyze_assessment(questions, answers)
