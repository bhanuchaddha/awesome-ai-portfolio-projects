"""
Generic Streamlit App Template for AI Agents

This module contains all Streamlit-specific UI code that can be reused across agents.
Import this module and call run_streamlit_app() with your agent's get_agent_response function.
"""

import streamlit as st
import asyncio
from typing import Callable, Awaitable


def run_streamlit_app(
    get_agent_response: Callable[[str], Awaitable[str]],
    agent_name: str,
    agent_icon: str = "🤖"
) -> None:
    """
    Run the Streamlit app with the provided agent function.
    
    Args:
        get_agent_response: Async function that takes a message string and returns response string
        agent_name: Display name for the agent
        agent_icon: Emoji icon for the agent (default: 🤖)
    """
    st.set_page_config(
        page_title=agent_name,
        page_icon=agent_icon,
        layout="wide"
    )

    st.title(f"{agent_icon} {agent_name}")

    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "response" not in st.session_state:
        st.session_state.response = None

    # Sidebar with reset button
    with st.sidebar:
        st.header("Controls")
        if st.button("🔄 Reset", use_container_width=True):
            st.session_state.messages = []
            st.session_state.response = None
            st.rerun()

    # Display conversation history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Main input area
    user_input = st.chat_input("Enter your message here...")

    if user_input:
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(user_input)
        
        # Get agent response
        with st.chat_message("assistant"):
            with st.spinner("Agent is thinking..."):
                try:
                    # Run async function
                    response = asyncio.run(get_agent_response(user_input))
                    
                    # Display response
                    st.markdown(response)
                    
                    # Save to session state
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    st.session_state.response = response
                    
                except Exception as e:
                    error_message = f"❌ Error: {str(e)}"
                    st.error(error_message)
                    st.session_state.messages.append({"role": "assistant", "content": error_message})
