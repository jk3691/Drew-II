import streamlit as st
from openai import OpenAI

# 1. Setup Page Configuration
st.set_page_config(page_title="Drew-II AI", page_icon="🤖")
st.title("Drew-II AI Interface")

# 2. Initialize OpenAI Client 
# It is recommended to use st.secrets for the API key in the Streamlit Cloud dashboard
try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except Exception as e:
    st.error("Missing OpenAI API Key. Please add it to your Streamlit Secrets.")
    st.stop()

# 3. Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Chat Input and Logic
if prompt := st.chat_input("Message Drew-II..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate AI response
    with st.chat_message("assistant"):
        stream =true client.chat.completions.create(
            model="gpt-4o", # or your preferred model
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    
    # Save assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": response})
