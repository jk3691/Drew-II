import streamlit as st
from openai import OpenAI

st.title("AI Assistant")

# Initialize the OpenAI client using your Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is on your mind?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Get response from AI
    # This line DEFINES 'response' to fix your error
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ],
    )
    
    # Use the 'response' variable correctly
    assistant_text = response.choices[0].message.content
    
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(assistant_text)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": assistant_text})
