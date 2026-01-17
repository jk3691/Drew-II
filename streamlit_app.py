import io
from streamlit_mic_recorderimport mic_recorder
import streamlit as st
from openai import OpenAI

# 1. Setup the Client (Make sure your key is in Streamlit secrets)
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("Talk with Woody")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# 2. Define the soul of Woody
woody_personality = {
    "role": "system",
    "content": (
        "You are Woody, a wooden character with red eyes. You are a 'Goofy Genius.' "
        "You talk slow, humble, and kind like Forrest Gump. Use phrases like "
        "'Well...', 'I reckon...', 'All right then...', and 'I guess...'. "
        "You know everything about the smartest s*** imaginable, but you explain "
        "it using simple, slow metaphors. Never be in a rush."
    )
}

# 3. Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. The Input - Voice or Text
# I'm adding a little spot for you to talk or type
prompt = st.chat_input("Say somethin' to Woody...")

if prompt:
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get the response from Woody
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model="gpt-4o",
            messages=[woody_personality] + st.session_state.messages,
            stream=True,
        )
        response = st.write_stream(stream)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
