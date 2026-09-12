import streamlit as st
from openai import OpenAI
import pyttsx3
from io import BytesIO
import os

# Show title and description.
st.set_page_config(page_title="Drew-II Research Agent", layout="wide")
st.title("🔬 Drew-II Research Agent")
st.write(
    "Your groovy research companion powered by AI. Select your preferred character and let's explore the cosmos of knowledge! "
    "To use this app, you need to provide an OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys)."
)

# Character definitions
characters = {
    "Hippie Science Professor": {
        "emoji": "🌼",
        "color": "#8B7355",
        "system_prompt": """You are a groovy, laid-back science professor from the 1970s who loves research and discovery. 
You speak in a friendly, conversational way with occasional hippie expressions like "Far out!", "That's groovy!", "Check it out, man", "Far as the research goes...".
You explain complex scientific concepts in a relatable, chill way. You're educational but approachable, and you genuinely love helping people understand science.
Keep responses engaging but informative. Use simple language without dumbing things down.""",
        "voice_id": 0,  # For text-to-speech voice selection
    }
}

# Ask user for their OpenAI API key
openai_api_key = st.text_input("OpenAI API Key", type="password")

if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:
    # Create an OpenAI client
    client = OpenAI(api_key=openai_api_key)
    
    # Sidebar for character selection and audio settings
    st.sidebar.header("⚙️ Settings")
    selected_character = st.sidebar.selectbox(
        "Choose your research guide:",
        list(characters.keys()),
        index=0
    )
    
    # Audio settings
    st.sidebar.subheader("🔊 Audio Settings")
    enable_tts = st.sidebar.checkbox("Enable Text-to-Speech", value=True)
    if enable_tts:
        tts_speed = st.sidebar.slider("Speech Speed", 0.5, 2.0, 1.0, step=0.1)
        tts_volume = st.sidebar.slider("Volume", 0.0, 1.0, 0.8, step=0.1)
    
    # Get character info
    character_info = characters[selected_character]
    
    # Display character info
    st.markdown(f"### {character_info['emoji']} {selected_character}")
    
    # Create a session state variable to store the chat messages
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "current_audio" not in st.session_state:
        st.session_state.current_audio = None
    
    # Display the existing chat messages
    for message in st.session_state.messages:
        if message["role"] == "user":
            with st.chat_message("user", avatar="👤"):
                st.markdown(message["content"])
        else:
            with st.chat_message("assistant", avatar=character_info["emoji"]):
                st.markdown(message["content"])
                
                # Display audio player if TTS is enabled and this is a response
                if enable_tts and "audio_data" in message:
                    col1, col2, col3 = st.columns([1, 2, 1])
                    with col1:
                        st.audio(message["audio_data"], format="audio/mp3")
                    with col2:
                        st.caption("🔊 Listen to the response")
    
    # Create a chat input field
    if prompt := st.chat_input("What would you like to research?"):
        
        # Store and display the current prompt
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)
        
        # Generate a response using the OpenAI API with character system prompt
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": character_info["system_prompt"]},
                *[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ]
            ],
            stream=True,
        )
        
        # Stream the response to the chat
        with st.chat_message("assistant", avatar=character_info["emoji"]):
            response = st.write_stream(stream)
        
        # Generate audio if TTS is enabled
        audio_data = None
        if enable_tts:
            try:
                # Initialize text-to-speech engine
                engine = pyttsx3.init()
                engine.setProperty('rate', 150 * tts_speed)  # Adjust speech rate
                engine.setProperty('volume', tts_volume)
                
                # Save to BytesIO object
                audio_buffer = BytesIO()
                engine.save_to_file(response, 'temp_audio.mp3')
                engine.runAndWait()
                
                # Read the generated file
                if os.path.exists('temp_audio.mp3'):
                    with open('temp_audio.mp3', 'rb') as audio_file:
                        audio_data = audio_file.read()
                    os.remove('temp_audio.mp3')
                    
                    # Display audio player
                    col1, col2, col3 = st.columns([1, 2, 1])
                    with col1:
                        st.audio(audio_data, format="audio/mp3")
                    with col2:
                        st.caption("🔊 Listen to the response")
            except Exception as e:
                st.warning(f"Could not generate audio: {str(e)}")
        
        # Store the response with audio data
        message_data = {"role": "assistant", "content": response}
        if audio_data:
            message_data["audio_data"] = audio_data
        st.session_state.messages.append(message_data)
