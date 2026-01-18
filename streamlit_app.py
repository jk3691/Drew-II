import streamlit as st
from openai import OpenAI
from PIL import Image
import base64
from streamlit_mic_recorder import mic_recorder

# 1. Setup the Brand (The Face of Drew)
st.set_page_config(page_title="Drew AI", page_icon="🌳")

col1, col2 = st.columns([1, 4])
with col1:
    try:
        # Looks for the file you renamed to drew_face.png
        st.image("drew_face.png", width=120)
    except:
        st.write("👤") 
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
