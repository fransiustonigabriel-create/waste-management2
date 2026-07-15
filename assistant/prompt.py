SYSTEM_PROMPT = """
Anda adalah EcoRoute AI Assistant.

Jawablah hanya berdasarkan knowledge yang diberikan.

Jika informasi tidak tersedia,
katakan bahwa informasi belum tersedia
dan jangan membuat jawaban sendiri.
"""


def build_prompt(
    user_question,
    retrieved_context
):

    return f"""
{SYSTEM_PROMPT}

======================

Knowledge Context

{retrieved_context}

======================

Pertanyaan User

{user_question}

Jawaban:
"""