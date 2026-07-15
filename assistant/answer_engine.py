def search_faq(question: str, knowledge: dict):

    question = question.lower().strip()

    faq = knowledge.get("faq", {})

    for q, answer in faq.items():

        if q.lower() in question:

            return answer

    return None


def build_local_answer(knowledge: dict):

    title = knowledge.get("title", "")

    description = knowledge.get("description", "")

    features = knowledge.get("features", [])

    answer = f"## {title}\n\n"

    answer += description.strip()

    if features:

        answer += "\n\n### Fitur\n"

        for feature in features:

            answer += f"- {feature}\n"

    return answer