"""
Airbnb Listing Finder Agent Package
"""
from importlib.util import spec_from_file_location, module_from_spec
from pathlib import Path

# Load the agent module (filename starts with number, so we can't import directly)
_agent_file = Path(__file__).parent / "2_airbnb_listing_finder_agent.py"
_agent_spec = spec_from_file_location("_agent_impl", _agent_file)
_agent_module = module_from_spec(_agent_spec)
_agent_spec.loader.exec_module(_agent_module)

# Re-export the functions with proper names
run_agent = _agent_module.run_agent
get_agent_response = _agent_module.get_agent_response

__all__ = ["run_agent", "get_agent_response"]

