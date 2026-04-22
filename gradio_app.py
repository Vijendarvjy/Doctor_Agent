
import gradio as gr
import os
from groq import Groq

# For local testing, ensure GROQ_API_KEY is set in your environment variables
# or use Colab secrets if deploying directly from Colab.
# For deployment to platforms like Hugging Face Spaces, set it as a Space secret.
GROQ_API_KEY = "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"

# Initialize the Groq client outside the function to avoid re-initialization on each call
client = None
LLAMA_MODEL = "llama3-8b-8192" # You can change this to a supported Groq model like "llama3-70b-8192"

# Check if API key is available and initialize client
if GROQ_API_KEY:
    client = Groq(
        api_key=GROQ_API_KEY,
    )
else:
    print("Warning: GROQ_API_KEY is not set. Please set it in your environment variables or Colab secrets.")

def generate_groq_response(user_message):
    """
    Queries the Groq model with a user's health inquiry and returns the response.

    Args:
        user_message (str): The user's health-related question or statement.

    Returns:
        str: The model's response to the inquiry.
    """
    if not client:
        return "Error: Groq API client not initialized. Please ensure GROQ_API_KEY is set."
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

# Gradio Interface
iface = gr.Interface(
    fn=generate_groq_response,
    inputs=gr.Textbox(
        label="Your health inquiry:",
        placeholder="I have a persistent cough and feel very tired. What could be causing this, and what over-the-counter medications might help?"
    ),
    outputs=gr.Markdown(
        label="AI Medical Assistant Response:"
    ),
    title="🩺 AI Medical Assistant powered by Groq (Gradio)",
    description="Ask me any health-related questions, and I'll do my best to provide helpful information (but remember, I'm an AI, not a doctor!).",
    examples=[
        ["I have a persistent cough and feel very tired. What could be causing this, and what over-the-counter medications might help?"],
        ["I'm feeling anxious lately, what are some simple relaxation techniques I can try?"],
        ["What are the benefits of drinking water daily?"],
    ],
    theme="huggingface"
)

if __name__ == "__main__":
    # Launch the Gradio app
    # Set share=True to get a public link (valid for 72 hours)
    # For deployment, consider setting a port if needed (e.g., port=7860)
    iface.launch(share=True)
