"""
Streamlit App for Competitor Analysis Agent

Run with: streamlit run streamlit_app.py
"""

import sys
from pathlib import Path
from importlib import import_module
from importlib.util import spec_from_file_location, module_from_spec

# Get the root directory and add it to the Python path to enable imports
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

# 1. Import the agent's get_agent_response function
#    Replace "5_competitor_analysis_agent" with your agent's package name.
agent_module_name = "5_competitor_analysis_agent.5_competitor_analysis_agent"
agent_file_path = Path(__file__).resolve().parent / "5_competitor_analysis_agent.py"
spec = spec_from_file_location(agent_module_name, agent_file_path)
agent_module = module_from_spec(spec)
spec.loader.exec_module(agent_module)
get_agent_response = agent_module.get_agent_response


# 2. Import the Streamlit UI from the common template
from common.streamlit_app_template import run_streamlit_app

# 3. Configure your agent's name and icon
AGENT_NAME = "Competitor Analysis Agent"
AGENT_ICON = "📈"
REQUIRED_SECRETS = ["FIRECRAWL_API_KEY"]

# Run the Streamlit app
run_streamlit_app(get_agent_response, AGENT_NAME, AGENT_ICON, REQUIRED_SECRETS)
