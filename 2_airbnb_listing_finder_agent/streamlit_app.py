"""
Streamlit App for Airbnb Listing Finder Agent

Run with: streamlit run streamlit_app.py
"""

import sys
from pathlib import Path
from importlib import import_module
from importlib.util import spec_from_file_location, module_from_spec

# Get the root directory (parent of agent directory)
# streamlit_app.py is in: enterprise-ai-agents/2_airbnb_listing_finder_agent/streamlit_app.py
# root_dir should be: enterprise-ai-agents/
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

# Import the agent's get_agent_response function from the package
# Note: Directory names starting with numbers require importlib
agent_package = import_module("2_airbnb_listing_finder_agent")
get_agent_response = agent_package.get_agent_response

# Import Streamlit UI from template in common package
# Using importlib to ensure it works reliably
template_file = root_dir / "common" / "streamlit_app_template.py"
if not template_file.exists():
    raise FileNotFoundError(f"Template file not found at: {template_file}")

template_spec = spec_from_file_location("streamlit_app_template", template_file)
template_module = module_from_spec(template_spec)
template_spec.loader.exec_module(template_module)
run_streamlit_app = template_module.run_streamlit_app

# Agent configuration
AGENT_NAME = "Airbnb Listing Finder Agent"
AGENT_ICON = "🏠"

# Run the Streamlit app (must be at module level for Streamlit)
run_streamlit_app(get_agent_response, AGENT_NAME, AGENT_ICON)
