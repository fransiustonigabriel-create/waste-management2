import streamlit as st

from assistant.assistant import EcoRouteAssistant

st.title("🤖 EcoRoute AI Assistant")
st.caption("EcoRoute AI Intelligent Assistant")

assistant = EcoRouteAssistant()

if "messages" not in st.session_state:
    st.session_state.messages = []

if "quick_question" not in st.session_state:
    st.session_state.quick_question = None

# ==========================
# Welcome
# ==========================

if len(st.session_state.messages) == 0:

    st.info(
        """
### 👋 Selamat Datang

Saya dapat membantu mengenai:

- 📊 Dashboard
- 🚛 Armada
- 🎛️ Event Simulator
- 🗺️ Routing
- 🤖 Machine Learning
- ♻️ Waste Management
"""
    )

# ==========================
# History
# ==========================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ==========================
# Input
# ==========================

prompt = st.chat_input(
    "Tanyakan sesuatu mengenai EcoRoute AI..."
)

if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        with st.spinner("🤖 EcoRoute AI sedang berpikir..."):

            result = assistant.ask(prompt)

            response = result["answer"]

            intent = result["intent"]

        st.markdown(response)

        st.divider()

        st.markdown("#### 💡 Pertanyaan Terkait")

        suggestions = assistant.suggestions(intent)

        cols = st.columns(len(suggestions))

        for i, question in enumerate(suggestions):

            with cols[i]:

                if st.button(question, key=f"{intent}_{i}"):

                    st.session_state.quick_question = question

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )

if st.session_state.quick_question:

    question = st.session_state.quick_question
    st.session_state.quick_question = None

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    st.rerun()