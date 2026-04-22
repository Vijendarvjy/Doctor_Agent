import streamlit as st
from groq import Groq

# -------------------------------
# LOAD API KEY (SECURE)
# -------------------------------
try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except KeyError:
    st.error("❌ GROQ_API_KEY not found in Streamlit secrets.")
    st.stop()

# -------------------------------
# INIT CLIENT
# -------------------------------
client = Groq(api_key=GROQ_API_KEY)

# Supported model
LLAMA_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"

# -------------------------------
# FUNCTION
# -------------------------------
def generate_groq_response(user_message):
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful medical assistant. Provide safe, general health guidance. Avoid diagnosis."},
                {"role": "user", "content": user_message}
            ],
            model=LLAMA_MODEL,
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"❌ Error: {e}"

# -------------------------------
# UI
# -------------------------------
st.set_page_config(page_title="AI Medical Assistant", page_icon="🩺")

st.title("🩺 AI Medical Assistant")
st.write(
    "Ask health-related questions. This tool provides general guidance only."
)

user_query = st.text_area(
    "Your health inquiry:",
    "I have a persistent cough and feel very tired. What could be causing this?"
)

if st.button("Get Advice"):
    if not user_query.strip():
        st.warning("⚠️ Please enter your health inquiry.")
    else:
        with st.spinner("Analyzing your symptoms..."):
            response = generate_groq_response(user_query)
            st.success("AI Response")
            st.write(response)

# -------------------------------
# DISCLAIMER
# -------------------------------
st.markdown("---")
st.warning(
    "⚠️ This AI assistant is for informational purposes only and not medical advice. "
    "Consult a qualified doctor for diagnosis or treatment."
)
