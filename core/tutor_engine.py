from core.llm_engine import generate
from core.prompts import tutor_prompt


def tutor_reply(profile, topic, mistakes, message, history):
    live = generate(tutor_prompt(profile, topic, mistakes, message, history),
                    "You are a patient, precise personal teacher.")
    if live:
        return live
    level = profile.get("learning_level", "Beginner") if profile else "Beginner"
    style = profile.get("explanation_style", "Simple explanations") if profile else "Simple explanations"
    mistakes_hint = f" Based on prior mistakes, focus on: {', '.join(mistakes[:2])}." if mistakes else ""
    return (f"Demo tutor mode: for **{topic}**, we can start with a small step. "
            f"At a {level.lower()} level and using {style.lower()}, first identify the key idea and example in the problem.{mistakes_hint} "
            "Try explaining what you think it means, then I will give a hint rather than the answer.")
