"""
Streamlit App for Bookey the Book Recommender Agent

Run with: streamlit run streamlit_app.py
"""

import sys
from pathlib import Path
from importlib import import_module

# Get the root directory and add it to the Python path to enable imports
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

# Import the agent's get_agent_response function from the package
# Note: Directory names starting with hyphens require importlib
agent_package = import_module("4-bookey_the_book_recommender_agent")
get_agent_response = agent_package.get_agent_response

# Import the Streamlit UI from the common template
from common.streamlit_app_template import run_streamlit_app

# Configure the agent's name, icon, and required secrets
AGENT_NAME = "Bookey the Book Recommender"
AGENT_ICON = "📚"
REQUIRED_SECRETS = ["EXA_API_KEY", "OPENROUTER_API_KEY"]  # This agent uses ExaTools and OpenRouter

# Run the Streamlit app
run_streamlit_app(
    get_agent_response,
    AGENT_NAME,
    AGENT_ICON,
    required_secrets=REQUIRED_SECRETS
)
