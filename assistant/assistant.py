from assistant.retriever import retrieve
from assistant.prompt import build_prompt
from assistant.llm import generate_response


class EcoRouteAssistant:

    def ask(self, question):

        knowledges = retrieve(question)

        context = ""

        for knowledge in knowledges:

            context += f"""

## {knowledge.get("title")}

{knowledge.get("description")}

"""

        prompt = build_prompt(

            user_question=question,

            retrieved_context=context

        )

        answer = generate_response(prompt)

        return answer