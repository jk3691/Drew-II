import streamlit as st
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
    # This is where we tell Drew what to say
    payload = {
        "script": {
            "type": "text",
            "input": text,
            "provider": {"type": "microsoft", "voice_id": "en-US-GuyNeural"}
        },
        "source_url": "https://path-to-your-drew-image.jpg" 
    }
    
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

st.title("Talking with Drew")
st.write("I'm not a smart man, but I know what love is... and I know how to use an API.")
