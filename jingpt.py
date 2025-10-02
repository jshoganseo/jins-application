from openai import OpenAI
import streamlit as st
import json
import os
import streamlit.components.v1 as components
from pathlib import Path


head = Path(__file__).parent if "__file__" in globals() else Path.cwd()
components.html(
        f"""
<script src="https://unpkg.com/@dotlottie/player-component@2.7.12/dist/dotlottie-player.mjs" type="module"></script>
<dotlottie-player src="https://lottie.host/319a32a8-113d-4c17-9d7d-fd6ee25c6334/UuMYUbBjUI.lottie" background="transparent" speed="1" style="width: 500px; height: 500px" loop autoplay></dotlottie-player>
""",
        height=500,
    )
st.title(":blue[_JinGPT_] 💻")

client = OpenAI(api_key=st.secrets["credentials"]["chat"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("How may I help beautiful?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})