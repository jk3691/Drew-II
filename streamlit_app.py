import io
from streamlit_mic_recorder import mic_recorder
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

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. The Chat Logic
if prompt := st.chat_input("Ask him somethin'..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get response from OpenAI
    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[woody_personality] + st.session_state.messages
        )
        answer = response.choices[0].message.content
        st.markdown(answer)
    
    # Add assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": answer})st.write("---")
audio = mic_recorder(
    start_prompt="Click to Talk 🎤",
    stop_prompt="Stop & Send 🛑",
    key='recorder'
)

if audio:
    audio_bytes = audio['bytes']
    with st.spinner("Listening..."):
        audio_file = io.BytesIO(audio_bytes)
        audio_file.name = "audio.wav"
        transcript = client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file
        )
        user_text = transcript.text
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": user_text}]
        )
        st.session_state.messages.append({"role": "user", "content": user_text})
        st.session_state.messages.append({"role": "assistant", "content": response.choices[0].message.content})
        st.rerun()

