"""
Generic Streamlit App Template for AI Agents

This module contains all Streamlit-specific UI code that can be reused across agents.
Import this module and call run_streamlit_app() with your agent's get_agent_response function.
"""

import streamlit as st
import asyncio
import os
from typing import Callable, Awaitable, List, Optional, Union
import inspect


def run_streamlit_app(
    get_agent_response: Callable[[str], Union[Awaitable[str], str]],
    agent_name: str,
    agent_icon: str = "🤖",
    required_secrets: Optional[List[str]] = None,
) -> None:
    """
    Run the Streamlit app with the provided agent function.
    
    Args:
        get_agent_response: Sync or async function that takes a message string and returns response string
        agent_name: Display name for the agent
        agent_icon: Emoji icon for the agent (default: 🤖)
        required_secrets: A list of secret keys to ask for in the sidebar (e.g., ["EXA_API_KEY"])
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

    # Sidebar with controls and secret inputs
    with st.sidebar:
        st.header("Controls")
        if st.button("🔄 Reset Chat", use_container_width=True):
            st.session_state.messages = []
            st.session_state.response = None
            st.rerun()

        if required_secrets:
            st.header("API Keys")

            # Check if all keys are already in session state
            keys_are_set = all(key in st.session_state for key in required_secrets)

            if keys_are_set:
                st.success("API keys are set for this session.")
                if st.button("Reset API Keys"):
                    for key in required_secrets:
                        if key in st.session_state:
                            del st.session_state[key]
                        if key in os.environ:
                            del os.environ[key]
                    st.rerun()
            else:
                st.write("Enter your API keys below to begin.")
                for secret_key in required_secrets:
                    if secret_key not in st.session_state:
                        key_value = st.text_input(
                            f"Enter your {secret_key}",
                            type="password",
                            key=f"input_{secret_key}",
                            help=f"This key will be set as the `{secret_key}` environment variable for this session."
                        )
                        if key_value:
                            st.session_state[secret_key] = key_value
                            # Rerun to update the UI and process other keys if needed
                            st.rerun()

            # Set environment variables from session state for the agent to use
            for key in required_secrets:
                if key in st.session_state:
                    os.environ[key] = st.session_state[key]

    # Display conversation history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Main input area
    user_input = st.chat_input("Enter your message here...")

    if user_input:
        # Check if all required secrets are provided before running
        missing_keys = [key for key in required_secrets if not os.getenv(key)] if required_secrets else []

        if missing_keys:
             st.error(f"Cannot run agent. Please provide the following required API keys in the sidebar: {', '.join(missing_keys)}")
        else:
            # Add user message to history
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            # Display user message
            with st.chat_message("user"):
                st.markdown(user_input)
            
            # Get agent response
            with st.chat_message("assistant"):
                with st.spinner("Agent is thinking..."):
                    try:
                        # Handle both sync and async agent functions
                        if inspect.iscoroutinefunction(get_agent_response):
                            response = asyncio.run(get_agent_response(user_input))
                        else:
                            response = get_agent_response(user_input)
                        
                        # Display response
                        st.markdown(response)
                        
                        # Save to session state
                        st.session_state.messages.append({"role": "assistant", "content": response})
                        st.session_state.response = response
                        
                    except Exception as e:
                        error_message = f"❌ Error: {str(e)}"
                        st.error(error_message)
                        st.session_state.messages.append({"role": "assistant", "content": error_message})
