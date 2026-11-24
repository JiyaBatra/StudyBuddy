def tutor_prompt(profile, topic, mistakes, message, history):
    level = profile.get("learning_level", "Beginner") if profile else "Beginner"
    style = profile.get("explanation_style", "Simple explanations") if profile else "Simple explanations"
    mistake_text = ", ".join(mistakes[:5]) if mistakes else "None recorded yet"
    return f"""Student level: {level}
Preferred explanation style: {style}
Current topic: {topic}
Previous mistakes: {mistake_text}
Recent conversation: {history[-6:] if history else 'No previous messages'}

Student message: {message}

Teach patiently and adapt to the level. Never reveal an answer when the student is expected to solve one; begin with a hint.
Use clear steps, ask a follow-up understanding check, and avoid unsupported claims about progress."""
