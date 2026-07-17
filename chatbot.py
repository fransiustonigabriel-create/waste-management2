import streamlit as st

from assistant.assistant import EcoRouteAssistant


# =========================================================
# Page Header
# =========================================================

st.title("🤖 EcoRoute AI Assistant")

st.caption(
    "Asisten cerdas untuk memahami fitur, prediksi, armada, "
    "routing, dan Machine Learning pada EcoRoute AI."
)


# =========================================================
# Assistant Instance
# =========================================================

assistant = EcoRouteAssistant()


# =========================================================
# Session State
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_question" not in st.session_state:
    st.session_state.pending_question = None

if "last_intent" not in st.session_state:
    st.session_state.last_intent = "general"


# =========================================================
# Helper: Normalize Assistant Result
# =========================================================

def normalize_result(result):
    """
    Menyamakan hasil EcoRouteAssistant.ask() agar UI tetap
    berjalan ketika hasilnya berupa dictionary atau string.
    """

    if isinstance(result, dict):
        return {
            "answer": result.get(
                "answer",
                "Maaf, jawaban belum tersedia.",
            ),
            "intent": result.get(
                "intent",
                "general",
            ),
            "response_type": result.get(
                "response_type",
                "general",
            ),
            "faq_matched": result.get(
                "faq_matched",
                False,
            ),
            "answer_mode": result.get(
                "answer_mode",
                "local",
            ),
            "recommendations": result.get(
                "recommendations",
                [],
            ),
            "risks": result.get(
                "risks",
                [],
            ),
            "sources": result.get(
                "sources",
                [],
            ),
            "ranking": result.get(
                "ranking",
                [],
            ),
            "confidence": result.get(
                "confidence",
                0,
            ),
            "sufficiency_reasons": result.get(
                "sufficiency_reasons",
                [],
            ),
        }

    if isinstance(result, str):
        return {
            "answer": result,
            "intent": "general",
            "response_type": "general",
            "faq_matched": False,
            "answer_mode": "local",
            "recommendations": [],
            "risks": [],
            "sources": [],
            "ranking": [],
            "confidence": 0,
            "sufficiency_reasons": [],
        }

    return {
        "answer": (
            "Maaf, sistem menghasilkan format jawaban "
            "yang tidak dikenali."
        ),
        "intent": "general",
        "response_type": "general",
        "faq_matched": False,
        "answer_mode": "error",
        "recommendations": [],
        "risks": [],
        "sources": [],
        "ranking": [],
        "confidence": 0,
        "sufficiency_reasons": [],
    }


# =========================================================
# Helper: Display Assistant Message
# =========================================================

def display_assistant_message(message):
    """
    Menampilkan jawaban utama serta panel informasi
    Adaptive Hybrid RAG dan Decision Engine.
    """

    content = message.get(
        "content",
        "Maaf, jawaban belum tersedia.",
    )

    st.markdown(content)

    try:
        confidence = int(
            message.get(
                "confidence",
                0,
            )
        )

    except (TypeError, ValueError):
        confidence = 0

    confidence = max(
        0,
        min(confidence, 100),
    )

    answer_mode = str(
        message.get(
            "answer_mode",
            "local",
        )
    )

    faq_matched = bool(
        message.get(
            "faq_matched",
            False,
        )
    )

    response_type = str(
        message.get(
            "response_type",
            "general",
        )
    )

    sufficiency_reasons = message.get(
        "sufficiency_reasons",
        [],
    )

    sources = message.get(
        "sources",
        [],
    )

    # =====================================================
    # Labels
    # =====================================================

    decision_labels = {
        "local": "🟢 Local Answer",
        "llm_fallback": "🟠 LLM Fallback",
        "out_of_domain": "🔴 Out of Domain",
        "error": "⚠️ Error",
    }

    response_type_labels = {
        "definition": "Definisi",
        "feature": "Fitur",
        "workflow": "Alur Kerja",
        "calculation": "Perhitungan",
        "recommendation": "Rekomendasi",
        "faq": "Frequently Asked Question (FAQ)",
        "comparison": "Perbandingan",
        "general": "Umum",
    }

    status_labels = {
        "local": (
            "Knowledge lokal dinilai memadai sehingga "
            "jawaban dapat disusun tanpa memanggil LLM."
        ),
        "llm_fallback": (
            "Knowledge lokal relevan, tetapi belum cukup untuk "
            "menjawab secara lengkap. Sistem menggunakan LLM "
            "untuk melakukan sintesis."
        ),
        "out_of_domain": (
            "Pertanyaan berada di luar ruang lingkup "
            "EcoRoute AI."
        ),
        "error": (
            "Terjadi masalah ketika sistem memproses "
            "pertanyaan."
        ),
    }

    # =====================================================
    # Confidence Labels
    # =====================================================

    if confidence >= 80:
        confidence_icon = "🟢"
        confidence_label = "Tinggi"

    elif confidence >= 50:
        confidence_icon = "🟡"
        confidence_label = "Sedang"

    else:
        confidence_icon = "🔴"
        confidence_label = "Rendah"

    # =====================================================
    # Information Panel
    # =====================================================

    with st.expander(
        "ℹ️ Informasi Jawaban",
        expanded=False,
    ):
        st.caption(
            "Informasi berikut menjelaskan bagaimana "
            "Adaptive Hybrid RAG memilih jalur jawaban."
        )

        col_1, col_2 = st.columns(2)

        with col_1:
            st.metric(
                "Confidence Knowledge Lokal",
                f"{confidence}%",
            )

        with col_2:
            st.metric(
                "FAQ Match",
                "Ya" if faq_matched else "Tidak",
            )

        col_3, col_4 = st.columns(2)

        with col_3:
            st.metric(
                "Decision Engine",
                decision_labels.get(
                    answer_mode,
                    answer_mode,
                ),
            )

        with col_4:
            st.metric(
                "Mode Sistem",
                "Adaptive Hybrid RAG",
            )

        st.markdown("---")

        st.markdown(
            f"**Jenis Respons:** "
            f"{response_type_labels.get(response_type, response_type)}"
        )

        st.markdown(
            f"**Status Confidence:** "
            f"{confidence_icon} {confidence_label} "
            f"({confidence}%)"
        )

        st.markdown(
            f"**Status Keputusan:** "
            f"{status_labels.get(answer_mode, 'Status tidak tersedia.')}"
        )

        if sufficiency_reasons:
            st.markdown("**Alasan Decision Engine:**")

            for reason in sufficiency_reasons:
                st.markdown(f"- {reason}")

        if sources:
            st.markdown("**Knowledge yang Digunakan:**")

            for source in sources:
                st.markdown(f"- {source}")


# =========================================================
# Helper: Process Question
# =========================================================

def process_question(question):
    """
    Memproses pertanyaan, menampilkan jawaban, dan menyimpan
    percakapan ke Streamlit Session State.
    """

    clean_question = str(question).strip()

    if not clean_question:
        return

    user_message = {
        "role": "user",
        "content": clean_question,
    }

    st.session_state.messages.append(
        user_message
    )

    with st.chat_message("user"):
        st.markdown(clean_question)

    with st.chat_message("assistant"):

        with st.spinner(
            "EcoRoute AI sedang menganalisis pertanyaan..."
        ):
            try:
                raw_result = assistant.ask(
                    clean_question
                )

                result = normalize_result(
                    raw_result
                )

            except Exception as error:
                result = {
                    "answer": (
                        "Maaf, terjadi kesalahan saat "
                        "memproses pertanyaan.\n\n"
                        f"**Detail:** `{error}`"
                    ),
                    "intent": "error",
                    "response_type": "general",
                    "faq_matched": False,
                    "answer_mode": "error",
                    "recommendations": [],
                    "risks": [],
                    "sources": [],
                    "ranking": [],
                    "confidence": 0,
                    "sufficiency_reasons": [],
                }

        assistant_message = {
            "role": "assistant",
            "content": result.get(
                "answer",
                "Maaf, jawaban belum tersedia.",
            ),
            "intent": result.get(
                "intent",
                "general",
            ),
            "response_type": result.get(
                "response_type",
                "general",
            ),
            "faq_matched": result.get(
                "faq_matched",
                False,
            ),
            "answer_mode": result.get(
                "answer_mode",
                "local",
            ),
            "recommendations": result.get(
                "recommendations",
                [],
            ),
            "risks": result.get(
                "risks",
                [],
            ),
            "sources": result.get(
                "sources",
                [],
            ),
            "ranking": result.get(
                "ranking",
                [],
            ),
            "confidence": result.get(
                "confidence",
                0,
            ),
            "sufficiency_reasons": result.get(
                "sufficiency_reasons",
                [],
            ),
        }

        display_assistant_message(
            assistant_message
        )

    st.session_state.messages.append(
        assistant_message
    )

    st.session_state.last_intent = result.get(
        "intent",
        "general",
    )


# =========================================================
# Welcome Screen
# =========================================================

if len(st.session_state.messages) == 0:

    with st.container(border=True):

        st.subheader("👋 Selamat datang")

        st.markdown(
            """
EcoRoute AI Assistant dapat membantu Anda mengenai:

- 📊 **Interactive Dashboard**
- 🚛 **Armada Management**
- 🎛️ **Event Simulator**
- 🗺️ **Routing**
- 🤖 **Machine Learning**
- ♻️ **Waste Management**

Pilih salah satu pertanyaan cepat atau ketik pertanyaan sendiri.
"""
        )

    row_1_col_1, row_1_col_2, row_1_col_3 = (
        st.columns(3)
    )

    with row_1_col_1:
        if st.button(
            "📊 Fungsi Dashboard",
            width="stretch",
            key="quick_dashboard",
        ):
            st.session_state.pending_question = (
                "Apa fungsi Interactive Dashboard?"
            )
            st.rerun()

    with row_1_col_2:
        if st.button(
            "🚛 Menghitung Armada",
            width="stretch",
            key="quick_armada",
        ):
            st.session_state.pending_question = (
                "Bagaimana cara menghitung kebutuhan armada?"
            )
            st.rerun()

    with row_1_col_3:
        if st.button(
            "🎛️ Event Simulator",
            width="stretch",
            key="quick_simulator",
        ):
            st.session_state.pending_question = (
                "Apa fungsi Event Simulator?"
            )
            st.rerun()

    row_2_col_1, row_2_col_2, row_2_col_3 = (
        st.columns(3)
    )

    with row_2_col_1:
        if st.button(
            "🗺️ Routing",
            width="stretch",
            key="quick_routing",
        ):
            st.session_state.pending_question = (
                "Bagaimana sistem menentukan rute armada?"
            )
            st.rerun()

    with row_2_col_2:
        if st.button(
            "🤖 Machine Learning",
            width="stretch",
            key="quick_ml",
        ):
            st.session_state.pending_question = (
                "Model Machine Learning apa yang digunakan "
                "EcoRoute AI?"
            )
            st.rerun()

    with row_2_col_3:
        if st.button(
            "♻️ Waste Management",
            width="stretch",
            key="quick_waste",
        ):
            st.session_state.pending_question = (
                "Bagaimana EcoRoute AI membantu "
                "pengelolaan sampah?"
            )
            st.rerun()


# =========================================================
# Display Chat History
# =========================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        if message["role"] == "assistant":
            display_assistant_message(
                message
            )

        else:
            st.markdown(
                message["content"]
            )


# =========================================================
# Process Quick Question
# =========================================================

if st.session_state.pending_question:

    queued_question = (
        st.session_state.pending_question
    )

    st.session_state.pending_question = None

    process_question(
        queued_question
    )


# =========================================================
# Chat Input
# =========================================================

user_prompt = st.chat_input(
    "Tanyakan sesuatu mengenai EcoRoute AI..."
)

if user_prompt:
    process_question(
        user_prompt
    )


# =========================================================
# Clear Conversation
# =========================================================

if st.session_state.messages:

    st.divider()

    if st.button(
        "🗑️ Hapus Percakapan",
        key="clear_chat",
    ):
        st.session_state.messages = []
        st.session_state.pending_question = None
        st.session_state.last_intent = "general"

        st.rerun()