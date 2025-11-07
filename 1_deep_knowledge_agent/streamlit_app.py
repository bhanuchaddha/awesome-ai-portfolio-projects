"""
Streamlit App for Deep Knowledge Agent

Run with: streamlit run streamlit_app.py
"""

import sys
from pathlib import Path
from importlib.util import spec_from_file_location, module_from_spec
import streamlit as st
from uuid import uuid4

# Get the root directory and add it to the Python path to enable imports
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

# 1. Import the agent's get_agent_response function
agent_module_name = "1_deep_knowledge_agent.1_deep_knowledge_agent"
agent_file_path = Path(__file__).resolve().parent / "1_deep_knowledge_agent.py"
spec = spec_from_file_location(agent_module_name, agent_file_path)
agent_module = module_from_spec(spec)
spec.loader.exec_module(agent_module)
get_agent_response_func = agent_module.get_agent_response


# 2. Import the Streamlit UI from the common template
from common.streamlit_app_template import run_streamlit_app

# 3. Configure your agent's name and icon
AGENT_NAME = "Deep Knowledge Agent"
AGENT_ICON = "📚"
REQUIRED_SECRETS = ["GOOGLE_API_KEY"]

# 4. Session management
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid4())

def get_response_with_session(message: str) -> str:
    """Wrapper to pass session_id to the agent."""
    return get_agent_response_func(message, st.session_state.session_id)

# Run the Streamlit app
run_streamlit_app(get_response_with_session, AGENT_NAME, AGENT_ICON, REQUIRED_SECRETS)
