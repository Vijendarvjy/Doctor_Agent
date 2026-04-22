
import streamlit as st
import os
from groq import Groq

# Load Groq API key from Streamlit secrets
# You need to set this in your Streamlit Cloud app's secrets:
GROQ_API_KEY="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"
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from .env file
load_dotenv()

# Get Groq API key from environment variables or Colab secrets
# If using Colab secrets, uncomment the line below and name your secret 'GROQ_API_KEY'
# GROQ_API_KEY = os.environ.get('GROQ_API_KEY') or userdata.get('GROQ_API_KEY')
#GROQ_API_KEY = "apikey"

# Initialize the Groq client
client = Groq(
    api_key=GROQ_API_KEY,
)

# Define the Llama model to use
LLAMA_MODEL = "openai/gpt-oss-120b" # Updated to a supported Llama model, e.g., "llama3-70b-8192"

print(f"Groq client initialized with model: {LLAMA_MODEL}")"
try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except KeyError:
    st.error("GROQ_API_KEY not found in Streamlit secrets. Please add it to your app's secrets.")
    st.stop() # Stop the app if API key is missing

# Define the Llama model to use
LLAMA_MODEL = "openai/gpt-oss-120b" # Ensure this model is supported by Groq

# Initialize the Groq client
client = Groq(api_key=GROQ_API_KEY)

def generate_groq_response(user_message):
    """
    Queries the Groq model with a user's health inquiry and returns the response.

    Args:
        user_message (str): The user's health-related question or statement.

    Returns:
        str: The model's response to the inquiry.
    """
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": user_message,
                }
            ],
            model=LLAMA_MODEL,
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {e}"

# Streamlit App UI
st.set_page_config(page_title="AI Medical Assistant powered by Groq")
st.title("🩺 AI Medical Assistant")
st.write("Ask me any health-related questions, and I'll do my best to provide helpful information (but remember, I'm an AI, not a doctor!).")

# User input
user_query = st.text_area("Your health inquiry:", "I have a persistent cough and feel very tired. What could be causing this, and what over-the-counter medications might help?")

if st.button("Get Advice"):
    if not user_query:
        st.warning("Please enter your health inquiry.")
    else:
        with st.spinner("Getting advice from the AI medical assistant..."):
            response = generate_groq_response(user_query)
            st.info("AI Response:")
            st.write(response)

st.markdown("---")
st.markdown("Disclaimer: This AI medical assistant is for informational purposes only and should not be considered medical advice. Always consult with a qualified healthcare professional for any health concerns.")
