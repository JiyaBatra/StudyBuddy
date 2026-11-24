def build_learning_plan(subject, weak, strong):
    weak = weak or ["Core foundations"]
    topics = []
    for concept in weak:
        topics.append({"topic": concept, "objective": f"Build understanding of {concept}",
                       "estimated_minutes": 25, "type": "revision", "completed": False})
    for concept in strong:
        topics.append({"topic": concept, "objective": f"Practice and retain {concept}",
                       "estimated_minutes": 15, "type": "extension", "completed": False})
    return {"subject": subject, "topics": topics,
            "strong_topics": strong, "weak_topics": weak,
            "estimated_time": sum(t["estimated_minutes"] for t in topics),
            "objectives": [t["objective"] for t in topics]}
