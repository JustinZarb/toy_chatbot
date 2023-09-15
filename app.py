import streamlit as st
import openai
import pandas as pd
import numpy as np
from datetime import datetime
import os
import json

st.title("ChatGPT-like clone")
st.markdown(
    "This is just a demo using the GPT-4 API and might break unexpectedly. You can download the conversation using the button below at any time. I don't keep a copy of what you write."
)
timestamp = datetime.now().strftime("%y%m%d.%H%M")

# export_conversation = "\n".join(st.session_state.messages)
if "messages" in st.session_state:
    export_conversation = json.dumps(st.session_state.messages)
else:
    export_conversation = ""
st.download_button(
    label="Download JSON",
    data=export_conversation,
    file_name=f"conversation_{timestamp}.json",
)


# Set OpenAI API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# Accept user input
if prompt := st.chat_input("What is up?"):
    """Doesn't work if this is hosted!
    # Save the prompt
    prompt_name = f"{timestamp}_user_prompt.txt"
    save_dir = "data/chats"
    save_path = os.path.join(save_dir, prompt_name)
    with open(save_path, "w") as f:
        f.write(prompt)
    """
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

    for response in openai.ChatCompletion.create(
        model=st.session_state["openai_model"],
        messages=[
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ],
        stream=True,
    ):
        full_response += response.choices[0].delta.get("content", "")
        message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
