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
from pathlib import Path
import base64


def _setup_page(agent_name: str, agent_icon: str):
    """Set up the Streamlit page configuration."""
    st.set_page_config(
        page_title=agent_name, page_icon=agent_icon, layout="wide"
    )
    st.title(f"{agent_icon} {agent_name}")


def _initialize_session_state():
    """Initialize session state variables."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "response" not in st.session_state:
        st.session_state.response = None


def _handle_file_upload():
    """Handle file upload and display preview."""
    st.header("File Upload")
    uploaded_file = st.file_uploader("Upload a file for the agent to use.", type=None)
    if uploaded_file is not None:
        upload_dir = Path("tmp/uploads")
        upload_dir.mkdir(parents=True, exist_ok=True)
        file_path = upload_dir / uploaded_file.name
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.session_state.uploaded_file_path = str(file_path)
        st.session_state.uploaded_file_details = {
            "name": uploaded_file.name,
            "type": uploaded_file.type,
        }
        st.success(f"Uploaded `{uploaded_file.name}`")

    if "uploaded_file_path" in st.session_state:
        st.subheader("File Preview")
        file_path_str = st.session_state.uploaded_file_path
        file_details = st.session_state.get("uploaded_file_details", {})
        file_type = file_details.get("type")
        file_name = file_details.get("name")

        if not file_type:
            st.warning("Could not determine file type for preview.")
        else:
            try:
                if file_type.startswith("image/"):
                    st.image(file_path_str, use_container_width=True)
                elif file_type == "application/pdf":
                    with open(file_path_str, "rb") as f:
                        base64_pdf = base64.b64encode(f.read()).decode("utf-8")
                    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="400" type="application/pdf"></iframe>'
                    st.markdown(pdf_display, unsafe_allow_html=True)
                elif file_type in [
                    "text/plain",
                    "text/markdown",
                    "text/csv",
                    "application/json",
                ]:
                    with open(
                        file_path_str, "r", encoding="utf-8", errors="ignore"
                    ) as f:
                        content = f.read(4096)  # read first 4KB
                    st.text_area("Preview (first 4KB)", content, height=300)
                    if len(content) == 4096:
                        st.caption("...")
                else:
                    st.info(f"No preview available for this file type ({file_type}).")
            except Exception as e:
                st.error(f"Error displaying preview for {file_name}: {e}")


def _manage_api_keys(required_secrets: List[str]):
    """Manage API key inputs and session state."""
    st.header("API Keys")
    
    # Check if keys are set in session state OR environment variables
    keys_are_set = all(
        (key in st.session_state) or (os.getenv(key) is not None) 
        for key in required_secrets
    )

    if keys_are_set:
        st.success("API keys are set for this session.")
        if st.button("Reset API Keys"):
            for key in required_secrets:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
    else:
        st.write("Enter your API keys below to begin.")
        for secret_key in required_secrets:
            # Only ask if not in session AND not in env
            if secret_key not in st.session_state and not os.getenv(secret_key):
                key_value = st.text_input(
                    f"Enter your {secret_key}",
                    type="password",
                    key=f"input_{secret_key}",
                    help=f"This key will be set as the `{secret_key}` environment variable for this session.",
                )
                if key_value:
                    st.session_state[secret_key] = key_value
                    st.rerun()

    # Ensure session keys are pushed to env for the current process
    for key in required_secrets:
        if key in st.session_state:
            os.environ[key] = st.session_state[key]


def _display_sidebar(required_secrets: Optional[List[str]], enable_file_uploader: bool):
    """Display the sidebar with controls, file uploader, and API key management."""
    with st.sidebar:
        st.header("Controls")
        if st.button("🔄 Reset Chat", use_container_width=True):
            st.session_state.messages = []
            st.session_state.response = None
            if "uploaded_file_path" in st.session_state:
                del st.session_state["uploaded_file_path"]
            if "uploaded_file_details" in st.session_state:
                del st.session_state["uploaded_file_details"]
            st.rerun()

        if required_secrets:
            _manage_api_keys(required_secrets)

        if enable_file_uploader:
            _handle_file_upload()


def _display_chat_history():
    """Display the chat history."""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def _handle_user_input(
    get_agent_response: Callable,
    enable_file_uploader: bool,
    required_secrets: Optional[List[str]],
):
    """Handle user input, get agent response, and display it."""
    user_input = st.chat_input("Enter your message here...")
    if user_input:
        missing_keys = (
            [key for key in required_secrets if not os.getenv(key)]
            if required_secrets
            else []
        )

        if missing_keys:
            st.error(
                f"Cannot run agent. Please provide the following required API keys in the sidebar: {', '.join(missing_keys)}"
            )
        else:
            st.session_state.messages.append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.markdown(user_input)

            with st.chat_message("assistant"):
                with st.spinner("Agent is thinking..."):
                    try:
                        agent_kwargs = {}
                        sig = inspect.signature(get_agent_response)
                        if (
                            enable_file_uploader
                            and "file_path" in sig.parameters
                            and "uploaded_file_path" in st.session_state
                        ):
                            agent_kwargs["file_path"] = st.session_state.get(
                                "uploaded_file_path"
                            )

                        if inspect.iscoroutinefunction(get_agent_response):
                            response = asyncio.run(
                                get_agent_response(user_input, **agent_kwargs)
                            )
                        else:
                            response = get_agent_response(user_input, **agent_kwargs)

                        st.markdown(response)
                        st.session_state.messages.append(
                            {"role": "assistant", "content": response}
                        )
                        st.session_state.response = response

                    except Exception as e:
                        error_message = f"❌ Error: {str(e)}"
                        st.error(error_message)
                        st.session_state.messages.append(
                            {"role": "assistant", "content": error_message}
                        )


def run_streamlit_app(
    get_agent_response: Callable,
    agent_name: str,
    agent_icon: str = "🤖",
    required_secrets: Optional[List[str]] = None,
    enable_file_uploader: bool = False,
) -> None:
    """
    Run the Streamlit app with the provided agent function.
    
    Args:
        get_agent_response: Sync or async function that takes a message string 
                            and optionally a `file_path` keyword argument.
        agent_name: Display name for the agent
        agent_icon: Emoji icon for the agent (default: 🤖)
        required_secrets: A list of secret keys to ask for in the sidebar (e.g., ["EXA_API_KEY"])
        enable_file_uploader: If True, a file uploader will be shown in the sidebar.
    """
    _setup_page(agent_name, agent_icon)
    _initialize_session_state()
    _display_sidebar(required_secrets, enable_file_uploader)
    _display_chat_history()
    _handle_user_input(get_agent_response, enable_file_uploader, required_secrets)
