import streamlit as st
import requests
import time

# 1. Setup the page
st.set_page_config(page_title="Talking Drew", page_icon="🌳")

# 2. This function talks to D-ID to make the video
def generate_drew_video(text):
    url = "https://api.d-id.com/talks"
    
    headers = {
        "Authorization": f"Basic {st.secrets['DID_API_KEY']}",
        "Content-Type": "application/json"
    }
    
    # This is where we tell Drew what to say
    # Make sure 'source_url' is a direct link to Drew's photo!
    payload = {
        "script": {
            "type": "text",
            "subtitles": "false",
            "provider": {"type": "microsoft", "voice_id": "en-US-GuyNeural"},
            "ssml": "false",
            "input": text
        },
        "config": {"fluent": "false", "pad_audio": "0.0"},
        "source_url": "https://create-images-results.d-id.com/Default_Presenters/Noel_m/image.jpg" 
    }

    response = requests.post(url, json=payload, headers=headers)
    return response.json()

# 3. The main part of the porch
st.title("Talking with Drew")
st.write("I'm not a smart man, but I know what love is... and I know how to use an API.")

# Input for the message
user_input = st.text_input("What should Drew say?", "Hello there, my name is Drew.")

if st.button("Make Drew Speak"):
    with st.spinner("Drew is thinking..."):
        # Create the talk
        data = generate_drew_video(user_input)
        
        if "id" in data:
            talk_id = data["id"]
            # We have to wait a lick for the video to finish processing
            status_url = f"https://api.d-id.com/talks/{talk_id}"
            headers = {"Authorization": f"Basic {st.secrets['DID_API_KEY']}"}
            
            while True:
                res = requests.get(status_url, headers=headers).json()
                if res.get("status") == "completed":
                    video_url = res.get("result_url")
                    st.video(video_url)
                    break
                elif res.get("status") == "error":
                    st.error("Something went wrong with the video.")
                    break
                time.sleep(2)
        else:
            st.error("Could not start the talk. Check your API key!")
