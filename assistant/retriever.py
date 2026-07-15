from assistant.intent import detect_intent
from assistant.knowledge_registry import KNOWLEDGE


def calculate_score(question, knowledge):

    score = 0

    title = knowledge.get("title", "").lower()

    description = knowledge.get("description", "").lower()

    question = question.lower()

    # ----------------------------------
    # Title Match (paling penting)
    # ----------------------------------

    if title in question:
        score += 15

    # ----------------------------------
    # Description Match
    # ----------------------------------

    for word in question.split():

        if len(word) < 3:
            continue

        if word in description:
            score += 2

    # ----------------------------------
    # FAQ Match
    # ----------------------------------

    faq = knowledge.get("faq", {})

    if isinstance(faq, dict):

        for key in faq.keys():

            key = key.lower()

            if key in question:

                score += 20

            else:

                for word in question.split():

                    if word in key:

                        score += 4

    # ----------------------------------
    # Related Topic
    # ----------------------------------

    topics = knowledge.get("related_topics", [])

    for topic in topics:

        topic = topic.lower()

        if topic in question:
            score += 6

    return score


def retrieve(question):

    question = question.lower()

    intent = detect_intent(question)

    ranked = []

    for name, knowledge in KNOWLEDGE.items():

        score = calculate_score(question, knowledge)

        if name == intent:
            score += 30

        ranked.append({

            "score": score,

            "knowledge": knowledge

        })

    ranked.sort(

        key=lambda x: x["score"],

        reverse=True

    )

    selected = []

    for item in ranked:

        if item["score"] <= 0:
            continue

        selected.append(item["knowledge"])

        if len(selected) == 3:
            break

    if len(selected) == 0:

        selected.append({

            "title": "General",

            "description":
                "Knowledge belum tersedia."

        })

    return selected