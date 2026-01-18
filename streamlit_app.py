import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

fig, ax = plt.subplots()
x = np.linspace(0, 2 * np.pi, 128)
line, = ax.plot(x, np.sin(x))

def update(frame):
    line.set_ydata(np.sin(x + frame / 10.0))
    return line,

ani = animation.FuncAnimation(fig, update, frames=100, blit=True)
ani.save('sine_wave.gif', writer='imagemagick') import streamlit as st
import requests
import time
import base64
from openai import OpenAI
from PIL import Image
from streamlit_mic_recorder import mic_recorder

# 1. Setup the Brand (The Face of Drew)
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
            "input": text,
            "provider": {"type": "microsoft", "voice_id": "en-US-GuyNeural"}
        }
    }
    
    # This sends the request and gets the reply
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

col1, col2 = st.columns([1, 2])

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
