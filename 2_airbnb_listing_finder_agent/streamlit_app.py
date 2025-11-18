"""
Streamlit App for Airbnb Listing Finder Agent

Run with: streamlit run streamlit_app.py
"""

import sys
from pathlib import Path
from importlib import import_module
from importlib.util import spec_from_file_location, module_from_spec
import streamlit as st
from uuid import uuid4
from typing import Optional
import asyncio

# Get the root directory (parent of agent directory)
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

# Import the agent's get_agent_response function from the package
agent_package = import_module("2_airbnb_listing_finder_agent")
get_agent_response_func = agent_package.get_agent_response

# Import Streamlit UI from template in common package
from common.streamlit_app_template import (
    run_streamlit_app,
    _initialize_session_state,
    _display_sidebar,
    _display_chat_history,
    _handle_user_input,
)
from common.openrouter_utils import get_free_models

# Agent configuration
AGENT_NAME = "Airbnb Listing Finder Agent"
AGENT_ICON = "🏠"
REQUIRED_SECRETS = ["OPENROUTER_API_KEY", "AIRBNB_MCP_API_KEY", "AIRBNB_MCP_PROFILE"]

# Session management
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid4())

async def get_response_with_session(message: str, file_path: Optional[str] = None) -> str:
    """Wrapper to pass session_id and model_id to the agent."""
    model_id = st.session_state.get("selected_model_id")
    # This agent function is async, so we await it.
    # The template's _handle_user_input checks for coroutine function and runs asyncio.run.
    return await get_agent_response_func(message, model_id=model_id)

# Custom page setup with logo
st.set_page_config(
    page_title=AGENT_NAME, 
    page_icon=AGENT_ICON, 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Header with logo
base_dir = Path(__file__).resolve().parent
logo_path = base_dir / "documentation" / "assets" / "agno.png"
demo_gif_path = base_dir / "documentation" / "assets" / "demo.gif"

col_title, col_logo = st.columns([4, 1])
with col_title:
    st.title(f"{AGENT_ICON} {AGENT_NAME}")
with col_logo:
    if logo_path.exists():
        st.image(str(logo_path), width=120)

# Overview Section
st.markdown("---")
st.markdown(
    """
    ### What This Agent Does
    
    The **Airbnb Listing Finder Agent** is an intelligent travel assistant that finds the perfect accommodation for your trip. 
    Instead of manually filtering through hundreds of listings, you can simply tell the agent what you're looking for in plain English.
    
    - **Understands complex requirements** (e.g., "apartment near Trivoli with a dedicated workspace")
    - **Searches and filters** real-time Airbnb listings
    - **Analyzes reviews and amenities** to ensure quality
    - **Presents top recommendations** with direct booking links
    
    **Perfect for:** Travelers, digital nomads, and travel planners who want to save time.
    """
)

# How it Works Section
with st.expander("How It Works - The Technology Behind the Agent", expanded=False):
    st.markdown(
        """
        ### The Search Process
        
        1. **Requirement Analysis**: The agent uses the **Think Tool** to map out your specific needs (dates, location, amenities, price).
        2. **Remote Search**: Connects to the **Airbnb MCP Server** hosted on Smithery.ai to fetch real-time listing data.
        3. **Intelligent Filtering**: Applies your criteria to filter down thousands of options.
        4. **Evaluation**: Analyzes the top candidates to select the best matches.
        5. **Presentation**: Displays the top 10 listings in a structured table with reasoning for each choice.
        
        ### Technology Stack
        
        | Component | Technology | Purpose |
        |-----------|-----------|---------|
        | **AI Framework** | Agno | Agent orchestration and reasoning |
        | **LLM Provider** | OpenRouter | Powers the agent's understanding (Llama 3, etc.) |
        | **Protocol** | MCP (Model Context Protocol) | Standardized interface to connect AI with remote services |
        | **Tooling** | Remote Airbnb MCP Server | Hosted service that provides Airbnb search capabilities |
        """
    )

# Quick Start Guide
with st.expander("Quick Start Guide", expanded=True):
    st.markdown(
        """

        ### Step 1: Describe Your Trip
        Tell the agent about your trip. Be specific about:
        - **Location**: City, neighborhood, or landmark
        - **Dates**: Check-in and check-out dates
        - **Guests**: Number of people
        - **Preferences**: Price range, room type, amenities (WiFi, pool, etc.)
        
        ### Step 2: Get Recommendations
        The agent will search and present a curated list of the best options!
        """
    )
    
    col1, col2 = st.columns([1, 1])
    with col1:
        if demo_gif_path.exists():
             # Using width="stretch" based on deprecation warning: "For use_container_width=True, use width='stretch'"
             st.image(str(demo_gif_path), caption="Agent finding listings in Copenhagen")
    with col2:
         st.markdown(
             """
             **Sample Query:**
             > "I'm traveling to Copenhagen from Jan 1st - Jan 8th. Can you find me the best deals for a 1 bedroom apartment? I'd like a dedicated workspace and close proximity to Trivoli."
             """
         )

# Use Cases Section
with st.expander("Use Cases", expanded=False):
    st.markdown(
        """
        - **Vacation Planning**: Find family-friendly homes near attractions.
        - **Business Travel**: Locate apartments with fast WiFi and workspaces.
        - **Budget Travel**: Find the best value stays within a specific budget.
        - **Group Trips**: Coordinate large villas for group events.
        """
    )

st.markdown("---")

_initialize_session_state()

# Sidebar Model Selection
with st.sidebar:
    st.header("Model Selection")
    with st.spinner("Fetching available free models..."):
        try:
            free_models = get_free_models()
            if free_models:
                model_names = list(free_models.keys())
                # Default to a known good model if available
                default_index = 0
                for i, name in enumerate(model_names):
                    if "llama" in name.lower() and "3" in name.lower():
                        default_index = i
                        break
                
                selected_model_name = st.selectbox(
                    "Choose a Model", 
                    model_names, 
                    index=default_index,
                    help="Select a free model from OpenRouter to power the agent."
                )
                st.session_state.selected_model_id = free_models[selected_model_name]
            else:
                st.warning("No free models found. Using default.")
                st.session_state.selected_model_id = None
        except Exception as e:
            st.error(f"Error fetching models: {e}")
            st.session_state.selected_model_id = None

_display_sidebar(REQUIRED_SECRETS, enable_file_uploader=False)
_display_chat_history()
_handle_user_input(
    get_response_with_session,
    enable_file_uploader=False,
    required_secrets=REQUIRED_SECRETS,
)
