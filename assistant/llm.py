from typing import Final

import streamlit as st
from google import genai
from google.genai import types


MODEL_NAME: Final[str] = "gemini-3.5-flash"

MAX_PROMPT_LENGTH: Final[int] = 12_000
REQUEST_TIMEOUT_MS: Final[int] = 60_000


def get_api_key() -> str:
    """
    Mengambil Gemini API key dari Streamlit secrets.
    """

    try:
        api_key = st.secrets["GEMINI_API_KEY"]

    except KeyError as error:
        raise RuntimeError(
            "GEMINI_API_KEY belum ditemukan di "
            ".streamlit/secrets.toml."
        ) from error

    except Exception as error:
        raise RuntimeError(
            "Streamlit tidak dapat membaca secrets.toml."
        ) from error

    api_key = str(api_key).strip()

    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY tersedia, tetapi nilainya kosong."
        )

    return api_key


def shorten_prompt(prompt: str) -> str:
    """
    Membatasi panjang prompt agar request lebih cepat
    dan tidak membawa context berlebihan.
    """

    clean_prompt = prompt.strip()

    if len(clean_prompt) <= MAX_PROMPT_LENGTH:
        return clean_prompt

    return (
        clean_prompt[:MAX_PROMPT_LENGTH]
        + "\n\n[Context dipotong karena terlalu panjang.]"
    )


def generate_response(prompt: str) -> str:
    """
    Mengirim prompt EcoRoute AI ke Gemini.
    """

    clean_prompt = shorten_prompt(prompt)

    if not clean_prompt:
        return (
            "Maaf, prompt untuk Gemini kosong sehingga "
            "jawaban belum dapat dibuat."
        )

    try:
        api_key = get_api_key()

        with genai.Client(
            api_key=api_key,
            http_options=types.HttpOptions(
                timeout=REQUEST_TIMEOUT_MS
            ),
        ) as client:

            interaction = client.interactions.create(
                model=MODEL_NAME,

                system_instruction=(
                    "Anda adalah EcoRoute AI Assistant, "
                    "asisten keputusan operasional untuk "
                    "pengelolaan sampah perkotaan. "
                    "Gunakan hanya informasi dari Knowledge "
                    "Context dan Operational Recommendation "
                    "yang terdapat di dalam input. "
                    "Jangan mengarang angka, lokasi, hasil model, "
                    "atau rekomendasi yang tidak tersedia. "
                    "Jawab dalam Bahasa Indonesia yang jelas, "
                    "ringkas, profesional, dan mudah dipahami. "
                    "Utamakan jawaban maksimal 3 paragraf atau "
                    "beberapa bullet singkat. "
                    "Jika informasi tidak tersedia, katakan "
                    "bahwa informasi tersebut belum tersedia."
                ),

                input=clean_prompt,

                generation_config={
                    "thinking_level": "low",
                    "temperature": 0.2,
                    "max_output_tokens": 500,
                },
            )

        answer = interaction.output_text

        if not answer or not answer.strip():
            return (
                "Gemini berhasil dihubungi, tetapi tidak "
                "menghasilkan jawaban teks."
            )

        return answer.strip()

    except Exception as error:
        error_text = str(error)

        if (
            "timeout" in error_text.lower()
            or "timed out" in error_text.lower()
        ):
            return (
                "Maaf, Gemini membutuhkan waktu terlalu lama "
                "untuk menjawab. Silakan coba kembali dengan "
                "pertanyaan yang lebih singkat."
            )

        return (
            "Maaf, EcoRoute AI belum dapat menghubungi Gemini.\n\n"
            f"**Detail:** `{error_text}`"
        )