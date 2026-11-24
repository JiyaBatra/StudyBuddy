def classify_mastery(score):
    if score >= 90:
        return "Strong mastery"
    if score >= 70:
        return "Good understanding"
    if score >= 40:
        return "Developing understanding"
    return "Needs foundational teaching"


def calculate_mastery(attempt_scores):
    if not attempt_scores:
        return 0
    weights = [0.5 * (0.75 ** i) for i in range(len(attempt_scores))]
    recent = list(reversed(attempt_scores))
    total = sum(value * weight for value, weight in zip(recent, weights))
    return round(total / sum(weights[:len(recent)]) * 100, 1)
