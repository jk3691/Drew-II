import io
import base64
from streamlit_mic_recorder import mic_recorder
import streamlit as st
from openai import OpenAI
from PIL import Image

# 1. Setup the Client (Make sure your key is in Streamlit secrets)
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("Talk with Drew")

# --- Image Upload Section ---
uploaded_file = st.file_uploader("Show Drew a picture...", type=["jpg", "jpeg", "png"])
if uploaded_file is not None:
    # Display the image so you can see it's there
    image = Image.open(uploaded_file)
    st.image(image, caption='What you showed Drew', use_container_width=True)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# 2. Define the soul of Drew
drew_personality = {
    "role": "system",
    "content": (
        "You are Drew, a character with red eyes. You are a 'Goofy Genius.' "
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

# --- Mic Recorder Section ---
st.write("Or tell Drew something:")
audio = mic_recorder(start_prompt="⏺️ Record", stop_prompt="⏹️ Stop", key='recorder')
# 4. Chat Input and Logic
if prompt := st.chat_input("Say something to Drew..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Prepare the message for the AI
    content = [{"type": "text", "text": prompt}]
    
    # If there's an image, add it to the request
    if uploaded_file is not None:
        base64_image = base64.b64encode(uploaded_file.getvalue()).decode('utf-8')
        content.append({
            "type": "image_url",
            "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
        })

    # Get Drew's response
    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            model="gpt-4o", # This model can see images
            messages=[
                drew_personality,
                *st.session_state.messages[:-1], # Past history
                {"role": "user", "content": content} # Current message + Image
            ]
        )
        full_response = response.choices[0].message.content
        st.markdown(full_response)
    
    # Save Drew's answer to history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
