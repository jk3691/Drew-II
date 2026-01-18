import streamlit as st
from openai import OpenAI
from PIL import Image
import base64
import requests
import time
from streamlit_mic_recorder import mic_recorder

# 1. Setup the Brand (The Face of Drew) - ONLY ONCE and AT THE TOP
st.set_page_config(page_title="Drew AI", page_icon="🌳")

# 2. This function talks to D-ID to make the video
def generate_drew_video(text):
    url = "https://api.d-id.com/talks"
    headers = {
        "Authorization": f"Basic {st.secrets['DID_API_KEY']}",
        "Content-Type": "application/json"
    }
    payload = {
        "script": {
            "type": "text",
            "provider": {"type": "microsoft", "voice_id": "en-US-GuyNeural"},
                    payload = {
            "script": {
                "type": "text",
                "provider": {"type": "microsoft", "voice_id": "en-US-GuyNeural"},
                "input": text
            },
            "source_url": "https://raw.githubusercontent.com/your-repo/main/drew_face.png"
        }

        "source_url": "https://raw.githubusercontent.com/your-repo/main/drew_face.png" # Link to Drew's photo
    }
    res = requests.post(url, json=payload, headers=headers)
    return res.json().get("id")

with col2:
    st.title("Drew AI")
    st.write("Take your time. I ain't in no rush.")

# 2. Connection & Personality
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []

# Updated Soul: Slow country accent, genius mind, no "Gump" references.
drew_personality = {
    "role": "system", 
    "content": (
        "You are Drew. You have a thick, slow country accent and use phrases like 'I reckon' and 'Well now'. "
        "You are a genius who knows everything about complex science, tech, and math, but you explain it "
        "slowly using simple metaphors. You are never in a hurry. You are kind and patient, but brilliant."
    )
}

# 3. Input Tools
uploaded_file = st.file_uploader("Show Drew a picture...", type=["jpg", "jpeg", "png"])
audio = mic_recorder(start_prompt="⏺️ Record", stop_prompt="⏹️ Stop", key='recorder')

# 4. Chat History Display
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if isinstance(message["content"], list):
            st.markdown(message["content"][0]["text"])
        else:
            st.markdown(message["content"])

# 5. Chat Logic
if prompt := st.chat_input("Say something to Drew..."):
    with st.chat_message("user"):
        st.markdown(prompt)

    message_content = [{"type": "text", "text": prompt}]
    
    if uploaded_file:
        base64_image = base64.b64encode(uploaded_file.getvalue()).decode('utf-8')
        message_content.append({
            "type": "image_url", 
            "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
        })

    st.session_state.messages.append({"role": "user", "content": message_content})

    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[drew_personality] + [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
        )
        full_response = response.choices[0].message.content
        st.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
