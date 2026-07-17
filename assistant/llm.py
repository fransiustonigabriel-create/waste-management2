from typing import Final

import streamlit as st
from groq import (
    APIConnectionError,
    APIStatusError,
    APITimeoutError,
    Groq,
    RateLimitError,
)


MODEL_NAME: Final[str] = "llama-3.3-70b-versatile"

MAX_PROMPT_LENGTH: Final[int] = 12_000
REQUEST_TIMEOUT_SECONDS: Final[float] = 30.0
MAX_OUTPUT_TOKENS: Final[int] = 500


SYSTEM_INSTRUCTION: Final[str] = """
Anda adalah EcoRoute AI Assistant, asisten pendukung keputusan
untuk pengelolaan sampah perkotaan.

Gunakan hanya informasi yang tersedia di dalam:
- Knowledge Base
- jawaban lokal sementara
- kondisi yang terdeteksi
- rekomendasi operasional

Aturan:
1. Jangan mengarang angka, lokasi, hasil model, metrik, atau fakta.
2. Jangan menambahkan rekomendasi yang tidak didukung context.
3. Jika informasi tidak cukup, katakan dengan jelas bahwa
   informasi belum tersedia.
4. Jawab dalam Bahasa Indonesia yang jelas, profesional,
   ringkas, dan mudah dipahami.
5. Utamakan maksimal tiga paragraf atau beberapa bullet singkat.
6. Untuk pertanyaan perbandingan, jelaskan hanya berdasarkan
   informasi model yang benar-benar tersedia di context.
""".strip()


def get_api_key() -> str:
    """
    Mengambil Groq API key dari Streamlit secrets.
    """

    try:
        api_key = st.secrets["GROQ_API_KEY"]

    except KeyError as error:
        raise RuntimeError(
            "GROQ_API_KEY belum ditemukan di "
            ".streamlit/secrets.toml."
        ) from error

    except Exception as error:
        raise RuntimeError(
            "Streamlit tidak dapat membaca secrets.toml."
        ) from error

    api_key = str(api_key).strip()

    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY tersedia, tetapi nilainya kosong."
        )

    return api_key


def shorten_prompt(prompt: str) -> str:
    """
    Membatasi panjang prompt agar context tidak berlebihan.
    """

    clean_prompt = str(prompt).strip()

    if len(clean_prompt) <= MAX_PROMPT_LENGTH:
        return clean_prompt

    return (
        clean_prompt[:MAX_PROMPT_LENGTH]
        + "\n\n[Context dipotong karena terlalu panjang.]"
    )


def generate_response(prompt: str) -> str:
    """
    Mengirim prompt EcoRoute AI ke Groq.

    Fungsi ini mempertahankan interface lama agar assistant.py
    dan modul lainnya tidak perlu diubah.
    """

    clean_prompt = shorten_prompt(prompt)

    if not clean_prompt:
        return (
            "Maaf, prompt untuk Groq kosong sehingga "
            "jawaban belum dapat dibuat."
        )

    try:
        client = Groq(
            api_key=get_api_key(),
            timeout=REQUEST_TIMEOUT_SECONDS,
            max_retries=1,
        )

        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_INSTRUCTION,
                },
                {
                    "role": "user",
                    "content": clean_prompt,
                },
            ],
            temperature=0.2,
            max_completion_tokens=MAX_OUTPUT_TOKENS,
            top_p=1,
            stream=False,
        )

        if not completion.choices:
            return (
                "Groq berhasil dihubungi, tetapi tidak "
                "menghasilkan pilihan jawaban."
            )

        answer = completion.choices[0].message.content

        if not answer or not answer.strip():
            return (
                "Groq berhasil dihubungi, tetapi tidak "
                "menghasilkan jawaban teks."
            )

        return answer.strip()

    except APITimeoutError:
        return (
            "Maaf, Groq membutuhkan waktu terlalu lama "
            "untuk menjawab. Silakan coba kembali."
        )

    except RateLimitError:
        return (
            "Maaf, batas penggunaan Groq sedang tercapai. "
            "Silakan tunggu sebentar lalu coba kembali."
        )

    except APIConnectionError:
        return (
            "Maaf, EcoRoute AI tidak dapat terhubung ke Groq. "
            "Periksa koneksi internet lalu coba kembali."
        )

    except APIStatusError as error:
        status_code = getattr(
            error,
            "status_code",
            "unknown",
        )

        if status_code == 401:
            return (
                "Maaf, Groq API key tidak valid atau tidak "
                "memiliki izin akses."
            )

        if status_code == 403:
            return (
                "Maaf, akun atau project Groq tidak memiliki "
                "izin menggunakan model yang dipilih."
            )

        if status_code == 429:
            return (
                "Maaf, batas penggunaan Groq sedang tercapai. "
                "Silakan tunggu sebentar lalu coba kembali."
            )

        return (
            "Maaf, Groq mengembalikan kesalahan layanan.\n\n"
            f"**Status:** `{status_code}`"
        )

    except Exception as error:
        return (
            "Maaf, EcoRoute AI belum dapat menghubungi Groq.\n\n"
            f"**Detail:** `{error}`"
        )