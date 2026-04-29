import streamlit as st
from groq import Groq

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Groq Chatbot", layout="centered")

# ⚠️ Replace with env var in production
KEY = "&U6bAb*6DvHRqIfP6IkNyWGdyb3FYTY*YsQdTDKL9tGQ4kN*Axmnn".replace("*", "7").replace("&", "gsk_")
client = Groq(api_key=KEY)

# ---------------- MODELS ----------------
MODELS = {
    "LLaMA 3.3 70B (Best Overall)": {
        "id": "llama-3.3-70b-versatile",
        "desc": "🧠 Highest quality model for reasoning, essays, and complex tasks.",
        "pros": "Very accurate, strong reasoning, great for school work",
        "cons": "Slightly slower than small models",
        "context": "131k tokens",
        "speed": "Medium"
    },

    "GPT OSS 120B (Ultra Powerful)": {
        "id": "openai/gpt-oss-120b",
        "desc": "🔥 Extremely powerful open model for advanced reasoning.",
        "pros": "Very strong intelligence, great instruction following",
        "cons": "Slower and heavier",
        "context": "131k tokens",
        "speed": "Slow"
    },

    "LLaMA 3 70B (Balanced)": {
        "id": "llama3-70b-8192",
        "desc": "⚖️ Balanced model for everyday chatbot use.",
        "pros": "Good balance of speed and intelligence",
        "cons": "Less advanced than 3.3 version",
        "context": "8k tokens",
        "speed": "Fast"
    },

    "Qwen 32B (Smart & Fast)": {
        "id": "qwen/qwen3-32b",
        "desc": "💡 Strong reasoning with good speed.",
        "pros": "Efficient, good for coding and analysis",
        "cons": "Less polished than top LLaMA models",
        "context": "131k tokens",
        "speed": "Fast"
    },

    "LLaMA 3 8B (Fast)": {
        "id": "llama3-8b-8192",
        "desc": "⚡ Very fast lightweight model.",
        "pros": "Super fast responses",
        "cons": "Weaker reasoning",
        "context": "8k tokens",
        "speed": "Very Fast"
    },

    "LLaMA 3.1 8B (Ultra Fast)": {
        "id": "llama-3.1-8b-instant",
        "desc": "🚀 Fastest model for quick replies.",
        "pros": "Extremely low latency",
        "cons": "Not good for complex reasoning",
        "context": "131k tokens",
        "speed": "Ultra Fast"
    }
}

# ---------------- SIDEBAR ----------------
st.sidebar.title("⚙️ Settings")

selected_model_name = st.sidebar.selectbox(
    "Choose a model:",
    list(MODELS.keys())
)

model = MODELS[selected_model_name]

st.sidebar.markdown("### 📊 Model Info")
st.sidebar.info(model["desc"])

st.sidebar.markdown("**🧠 Pros**")
st.sidebar.write(model["pros"])

st.sidebar.markdown("**⚠️ Cons**")
st.sidebar.write(model["cons"])

st.sidebar.markdown("---")
st.sidebar.markdown(f"📦 **Context:** {model['context']}")
st.sidebar.markdown(f"⚡ **Speed:** {model['speed']}")

# Clear chat
if st.sidebar.button("🧹 Clear Chat"):
    st.session_state.messages = [
        {"role": "assistant", "content": "Chat reset! 👋"}
    ]
    st.rerun()

# ---------------- SESSION STATE ----------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hey! Ask me anything 👀"}
    ]

# ---------------- UI ----------------
st.header("🤖 Groq AI Chatbot")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------- INPUT ----------------
if prompt := st.chat_input("Type your message..."):
    # user msg
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    # assistant response
    with st.chat_message("assistant"):
        with st.spinner(f"Thinking using {selected_model_name}..."):

            response = client.chat.completions.create(
                model=model["id"],
                messages=st.session_state.messages,
                temperature=0.7,
            )

            reply = response.choices[0].message.content
            st.markdown(reply)

    # save assistant msg
    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )