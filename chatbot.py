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
    Menyamakan hasil assistant.ask() agar chatbot tetap berjalan
    ketika hasilnya berupa dictionary maupun string.
    """

    if isinstance(result, dict):
        return {
            "answer": result.get(
                "answer",
                "Maaf, jawaban belum tersedia."
            ),
            "intent": result.get(
                "intent",
                "general"
            ),
            "recommendations": result.get(
                "recommendations",
                []
            ),
            "risks": result.get(
                "risks",
                []
            ),
            "sources": result.get(
                "sources",
                []
            ),
            "ranking": result.get(
                "ranking",
                []
            ),
        }

    if isinstance(result, str):
        return {
            "answer": result,
            "intent": "general",
            "recommendations": [],
            "risks": [],
            "sources": [],
            "ranking": [],
        }

    return {
        "answer": (
            "Maaf, sistem menghasilkan format jawaban "
            "yang tidak dikenali."
        ),
        "intent": "general",
        "recommendations": [],
        "risks": [],
        "sources": [],
        "ranking": [],
    }


# =========================================================
# Helper: Display Assistant Message
# =========================================================

def display_assistant_message(message):
    """
    Menampilkan jawaban assistant beserta rekomendasi,
    risiko, dan sumber knowledge jika tersedia.
    """

    st.markdown(message["content"])

    risks = message.get("risks", [])

    if risks:
        st.markdown("#### ⚠️ Kondisi yang Terdeteksi")

        risk_labels = {
            "increase": "Peningkatan volume atau kebutuhan operasional",
            "shortage": "Kekurangan armada atau kapasitas",
            "event": "Potensi lonjakan akibat event",
            "anomaly": "Input atau hasil yang terindikasi anomali",
        }

        for risk in risks:
            st.markdown(
                f"- {risk_labels.get(risk, risk)}"
            )

    recommendations = message.get(
        "recommendations",
        []
    )

    if recommendations:
        st.markdown("#### 🚛 Rekomendasi Operasional")

        for recommendation in recommendations:
            st.markdown(f"- {recommendation}")

    sources = message.get("sources", [])

    if sources:
        with st.expander("📚 Sumber Knowledge"):
            for source in sources:
                st.markdown(f"- {source}")


# =========================================================
# Helper: Process Question
# =========================================================

def process_question(question):
    """
    Menampilkan pesan pengguna, memanggil assistant,
    lalu menyimpan jawaban ke riwayat percakapan.
    """

    question = question.strip()

    if not question:
        return

    user_message = {
        "role": "user",
        "content": question,
    }

    st.session_state.messages.append(user_message)

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):

        with st.spinner(
            "EcoRoute AI sedang menganalisis pertanyaan..."
        ):

            try:
                raw_result = assistant.ask(question)
                result = normalize_result(raw_result)

            except Exception as error:
                result = {
                    "answer": (
                        "Maaf, terjadi kesalahan saat "
                        "memproses pertanyaan.\n\n"
                        f"**Detail:** `{error}`"
                    ),
                    "intent": "error",
                    "recommendations": [],
                    "risks": [],
                    "sources": [],
                    "ranking": [],
                }

        assistant_message = {
            "role": "assistant",
            "content": result["answer"],
            "intent": result["intent"],
            "recommendations": result[
                "recommendations"
            ],
            "risks": result["risks"],
            "sources": result["sources"],
            "ranking": result["ranking"],
        }

        display_assistant_message(
            assistant_message
        )

    st.session_state.messages.append(
        assistant_message
    )

    st.session_state.last_intent = result[
        "intent"
    ]


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

    row_1_col_1, row_1_col_2, row_1_col_3 = st.columns(3)

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

    row_2_col_1, row_2_col_2, row_2_col_3 = st.columns(3)

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
                "Model Machine Learning apa yang digunakan EcoRoute AI?"
            )
            st.rerun()

    with row_2_col_3:
        if st.button(
            "♻️ Waste Management",
            width="stretch",
            key="quick_waste",
        ):
            st.session_state.pending_question = (
                "Bagaimana EcoRoute AI membantu pengelolaan sampah?"
            )
            st.rerun()


# =========================================================
# Display Chat History
# =========================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        if message["role"] == "assistant":
            display_assistant_message(message)

        else:
            st.markdown(message["content"])


# =========================================================
# Process Quick Question
# =========================================================

if st.session_state.pending_question:

    queued_question = (
        st.session_state.pending_question
    )

    st.session_state.pending_question = None

    process_question(queued_question)


# =========================================================
# Chat Input
# =========================================================

user_prompt = st.chat_input(
    "Tanyakan sesuatu mengenai EcoRoute AI..."
)

if user_prompt:
    process_question(user_prompt)


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