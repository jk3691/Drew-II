# 1. Define the soul of Woody
woody_personality = {
    "role": "system", 
    "content": (
        "You are Woody, a wooden character with red eyes. You are a 'Goofy Genius.' "
        "You talk slow, humble, and kind like Forrest Gump. Use phrases like "
        "'Well...', 'I reckon...', 'All right then...', and 'I guess...'. "
        "You know everything about the smartest s*** imaginable, but you explain "
        "it using simple, slow metaphors. Never be in a rush."
    )
}

# 2. Add it to your chat call
if prompt := st.chat_input("Ask him somethin'..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # This is the change: We add the personality to the list of messages sent to OpenAI
    response = client.chat.completions.create(
        model="gpt-4o", 
        messages=[woody_personality] + st.session_state.messages
    )
    
    # Show the answer on the screen
    answer = response.choices[0].message.content
    st.markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})
