import streamlit as st
from datetime import datetime
import random
import time
from core_interface.Core import Core


class StreamlitInterface:

    def __init__(self) -> None:
        st.title("EHR-Llama ChatBot 🩺☤")
        self.core_inst = Core()

    def generate_response(self, user_query):
        response = self.core_inst.core_impl(user_query)
        for word in response.split():
            yield word + " "
            time.sleep(0.05)

    def start_chat(self):
        # Ensure the session state for messages is initialized
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Display existing messages from the session state (if any)
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Get input from the user to initiate the chat
        prompt = st.chat_input("Type your message here...")

        # Only proceed if the user has entered a message (i.e., chat is user-initiated)
        if prompt:
            # Display user's message
            with st.chat_message("user"):
                st.markdown(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})

            # Generate and display assistant's response
            with st.chat_message("assistant"):
                response = st.write_stream(self.generate_response(prompt))

            # Save the assistant's response in session state
            st.session_state.messages.append({"role": "assistant", "content": response})
