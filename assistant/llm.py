def generate_response(prompt: str) -> str:
    """
    Dummy LLM sementara.

    Nanti fungsi ini akan diganti menjadi
    Gemini / OpenAI tanpa mengubah file lain.
    """

    prompt = prompt.strip()

    if len(prompt) > 300:
        prompt_preview = prompt[:300] + "..."
    else:
        prompt_preview = prompt

    return f"""
🤖 EcoRoute AI (Development Mode)

Knowledge Base berhasil dimuat.

System Prompt berhasil dibuat.

Prompt Preview
----------------------------

{prompt_preview}

----------------------------

AI Model belum dihubungkan.

Tahap berikutnya adalah integrasi Gemini/OpenAI.
"""