import streamlit as st
from openai import OpenAI

# Initialize the client using Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("AI Assistant")

# Test message
if st.button("Test AI"):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": "Hello! Are you working?"}]
    )
    st.write(response.choices[0].message.content)
