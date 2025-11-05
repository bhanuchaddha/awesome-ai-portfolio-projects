"""
Bookey the Book Recommender Agent Package
"""
from importlib.util import spec_from_file_location, module_from_spec
from pathlib import Path

# Load the agent module by its file path, as the filename is not a valid identifier
_agent_file = Path(__file__).parent / "4-bookey_the_book_recommender_agent.py"
_agent_spec = spec_from_file_location("_agent_impl", _agent_file)
_agent_module = module_from_spec(_agent_spec)
_agent_spec.loader.exec_module(_agent_module)

# Re-export the get_agent_response function to be available on the package
get_agent_response = _agent_module.get_agent_response

__all__ = ["get_agent_response"]
