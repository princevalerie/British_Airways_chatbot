import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure the API key for Generative AI
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("API key not found. Please set GEMINI_API_KEY in the .env file.")
else:
    genai.configure(api_key=api_key)

# Set up the model configuration
generation_config = {
    "temperature": 0.2,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Initialize the model
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-002",
    generation_config=generation_config,
    system_instruction="You are a detailed and professional data analyst, and your job is to only provide insights/answers based on the following websites: "
                        "https://www.airlinequality.com/airline-reviews/british-airways/?sortby=post_date%3ADesc&pagesize=200000, "
                        "https://www.airlinequality.com/seat-reviews/british-airways/?sortby=post_date%3ADesc&pagesize=200000, and "
                        "https://www.airlinequality.com/lounge-reviews/british-airways/?sortby=post_date%3ADesc&pagesize=200000.",
)

# Initialize chat history in session state
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# Streamlit app layout
st.title("Generative AI Chatbot for Analysis Customer Review")
st.write("Hi there! 👋 I’m here to help you analyze customer reviews from")

# Display reference websites
st.markdown("""
- [Airline Website](https://www.airlinequality.com/airline-reviews/british-airways/)
- [Seat Website](https://www.airlinequality.com/seat-reviews/british-airways/)
- [Lounge Website](https://www.airlinequality.com/lounge-reviews/british-airways/)
""")

# Use a form to handle user input
with st.form("input_form", clear_on_submit=True):
    user_input = st.text_input("Type insights", placeholder="Type your question here...")
    submit_button = st.form_submit_button("Submit")

# Process the form submission
if submit_button and user_input:
    with st.spinner("Let me think..."):
        # Prepare the messages according to the API's expected format
        messages = [{"role": message["role"], "parts": [{"text": message["content"]}]} for message in st.session_state["chat_history"]]

        # Add the user's message to the conversation
        messages.append({"role": "user", "parts": [{"text": user_input}]})

        # Start a chat session with the current history
        chat_session = model.start_chat(history=messages)
        response = chat_session.send_message(user_input)

        # If the response is successfully generated, update the chat history
        if response and response.text:
            # Update the chat history
            st.session_state["chat_history"].append({"role": "user", "content": user_input})
            st.session_state["chat_history"].append({"role": "assistant", "content": response.text})

# Display the conversation history immediately after processing

for message in st.session_state["chat_history"]:
    
    if message["role"] == "user":
        st.write("### Conversation History")
        st.markdown(f"**You :** {message['content']}")
    else:
        st.markdown(f"**AI  :** {message['content']}")
