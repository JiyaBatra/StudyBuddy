def analyze_assessment(questions, answers):
    weak, strong = [], []
    correct = 0
    for question, answer in zip(questions, answers):
        expected = str(question.get("answer", "")).strip().lower()
        given = str(answer).strip().lower()
        concept = question.get("concept", question.get("topic", "General concept"))
        if question.get("type") == "multiple_choice":
            is_correct = given == expected
        else:
            is_correct = bool(given) and expected in given
        if is_correct:
            correct += 1
            if concept not in strong:
                strong.append(concept)
        elif concept not in weak:
            weak.append(concept)
    score = round(correct / len(questions) * 100, 1) if questions else 0
    return {"score": score, "weak_concepts": weak, "strong_concepts": strong,
            "correct_count": correct, "incorrect_count": len(questions) - correct}
