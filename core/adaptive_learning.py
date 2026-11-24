def next_difficulty(recent_correct):
    if not recent_correct:
        return "Easy"
    accuracy = sum(recent_correct) / len(recent_correct)
    if accuracy >= 0.8:
        return "Hard"
    if accuracy >= 0.5:
        return "Medium"
    return "Easy"
