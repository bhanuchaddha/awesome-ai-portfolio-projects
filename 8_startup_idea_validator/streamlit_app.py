"""
Streamlit App for Startup Idea Validator

Run with: streamlit run streamlit_app.py
"""
import streamlit as st
from pathlib import Path
import sys
import asyncio
import os
from importlib.util import spec_from_file_location, module_from_spec

# Get the root directory and add it to the Python path to enable imports
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

# Import common utilities
from common.openrouter_utils import get_free_models_list

# Import the agent's functions
agent_module_name = "8_startup_idea_validator.8_startup_idea_validator"
agent_file_path = Path(__file__).resolve().parent / "8_startup_idea_validator.py"
spec = spec_from_file_location(agent_module_name, agent_file_path)
agent_module = module_from_spec(spec)
spec.loader.exec_module(agent_module)
validate_startup_idea = agent_module.validate_startup_idea


# Page config
st.set_page_config(
    page_title="Startup Idea Validator",
    page_icon="🚀",
    layout="wide"
)

# Initialize session state
if "results" not in st.session_state:
    st.session_state.results = None
if "processing" not in st.session_state:
    st.session_state.processing = False
if "current_idea" not in st.session_state:
    st.session_state.current_idea = ""
if "selected_model_id" not in st.session_state:
    st.session_state.selected_model_id = None
if "free_models" not in st.session_state:
    st.session_state.free_models = []


def check_api_keys():
    """Check if required API keys are set."""
    required_keys = ["OPENROUTER_API_KEY", "EXA_API_KEY"]
    missing_keys = []
    
    for key in required_keys:
        if key not in st.session_state:
            if key in os.environ:
                st.session_state[key] = os.environ[key]
            else:
                missing_keys.append(key)
    
    return missing_keys


def get_field(obj, field_name, default=""):
    """Helper to get field from either dict or Pydantic model."""
    if obj is None:
        return default
    if isinstance(obj, dict):
        return obj.get(field_name, default)
    return getattr(obj, field_name, default)


def display_results(result):
    """Display the validation results."""
    if "error" in result:
        st.error(result['error'])
        return
    
    # Get results (could be dicts or Pydantic models)
    idea_clarification = result.get('idea_clarification')
    market_research = result.get('market_research')
    competitor_analysis = result.get('competitor_analysis')
    validation_report = result.get('validation_report')
    
    # Display comprehensive report
    st.markdown("# Startup Validation Report")
    
    # Executive Summary
    if validation_report:
        st.markdown("## Executive Summary")
        st.info(get_field(validation_report, 'executive_summary'))
        st.markdown("---")
    
    # Create tabs for different sections
    tab1, tab2, tab3, tab4 = st.tabs([
        "Idea Assessment",
        "Market Opportunity", 
        "Competitive Landscape",
        "Recommendations & Next Steps"
    ])
    
    with tab1:
        st.markdown("## Idea Assessment")
        
        if validation_report:
            st.markdown(get_field(validation_report, 'idea_assessment'))
        
        if idea_clarification:
            st.markdown("### Idea Clarification")
            
            with st.expander("Originality Analysis", expanded=True):
                st.markdown(get_field(idea_clarification, 'originality'))
            
            with st.expander("Mission Statement", expanded=True):
                st.success(get_field(idea_clarification, 'mission'))
            
            with st.expander("Objectives", expanded=True):
                st.markdown(get_field(idea_clarification, 'objectives'))
    
    with tab2:
        st.markdown("## Market Opportunity")
        
        if validation_report:
            st.markdown(get_field(validation_report, 'market_opportunity'))
        
        if market_research:
            st.markdown("### Market Size Analysis")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("#### TAM")
                st.markdown("*Total Addressable Market*")
                st.info(get_field(market_research, 'total_addressable_market'))
            
            with col2:
                st.markdown("#### SAM")
                st.markdown("*Serviceable Available Market*")
                st.info(get_field(market_research, 'serviceable_available_market'))
            
            with col3:
                st.markdown("#### SOM")
                st.markdown("*Serviceable Obtainable Market*")
                st.info(get_field(market_research, 'serviceable_obtainable_market'))
            
            st.markdown("### Target Customer Segments")
            st.markdown(get_field(market_research, 'target_customer_segments'))
    
    with tab3:
        st.markdown("## Competitive Landscape")
        
        if validation_report:
            st.markdown(get_field(validation_report, 'competitive_landscape'))
        
        if competitor_analysis:
            st.markdown("### Identified Competitors")
            st.markdown(get_field(competitor_analysis, 'competitors'))
            
            st.markdown("### SWOT Analysis")
            st.markdown(get_field(competitor_analysis, 'swot_analysis'))
            
            st.markdown("### Competitive Positioning")
            st.success(get_field(competitor_analysis, 'positioning'))
    
    with tab4:
        st.markdown("## Strategic Recommendations")
        
        if validation_report:
            st.markdown(get_field(validation_report, 'recommendations'))
            
            st.markdown("---")
            
            st.markdown("## Next Steps")
            st.markdown(get_field(validation_report, 'next_steps'))
            
            st.warning("**Disclaimer:** This validation is for informational purposes only. Conduct additional due diligence before making investment decisions.")


# Main app
def main():
    st.title("🚀 Startup Idea Validator")
    st.markdown("AI-powered validation system for entrepreneurs and founders")
    
    # Sidebar for API keys
    with st.sidebar:
        st.header("Configuration")
        
        missing_keys = check_api_keys()
        
        if missing_keys:
            st.warning("Please provide your API keys")
            for key in missing_keys:
                api_key = st.text_input(
                    f"Enter your {key}",
                    type="password",
                    key=f"input_{key}"
                )
                if api_key:
                    st.session_state[key] = api_key
                    os.environ[key] = api_key
                    st.rerun()
        else:
            st.success("API keys configured")
            if st.button("Reset API Keys"):
                for key in ["OPENROUTER_API_KEY", "EXA_API_KEY"]:
                    if key in st.session_state:
                        del st.session_state[key]
                    if key in os.environ:
                        del os.environ[key]
                st.rerun()
        
        st.markdown("---")
        st.markdown("### Model Selection")
        
        # Fetch free models if not already loaded
        if not st.session_state.free_models:
            with st.spinner("Loading available models..."):
                st.session_state.free_models = get_free_models_list()
        
        if st.session_state.free_models:
            # Create a list of model names for display
            model_options = [f"{model['name']}" for model in st.session_state.free_models]
            model_ids = [model['id'] for model in st.session_state.free_models]
            
            # Set default to minimax if available
            default_index = 0
            for i, model_id in enumerate(model_ids):
                if "minimax" in model_id.lower():
                    default_index = i
                    break
            
            selected_index = st.selectbox(
                "Choose OpenRouter Model",
                range(len(model_options)),
                format_func=lambda i: model_options[i],
                index=default_index,
                help="Select the AI model to use for validation"
            )
            
            st.session_state.selected_model_id = model_ids[selected_index]
            st.caption(f"Model ID: `{st.session_state.selected_model_id}`")
            
            if st.button("Refresh Models", use_container_width=True):
                st.session_state.free_models = get_free_models_list()
                st.rerun()
        else:
            st.error("Failed to load models. Using default model.")
            st.session_state.selected_model_id = "minimax/minimax-m2:free"
        
        st.markdown("---")
        st.markdown("### About")
        st.markdown(
            "This validator analyzes your startup idea through:\n\n"
            "- Idea Clarification\n"
            "- Market Research\n"
            "- Competitor Analysis\n"
            "- Strategic Recommendations"
        )
        
        st.markdown("---")
        st.markdown("### Example Ideas")
        st.caption("Click to use:")
        
        if st.button("AI-powered fitness coach", use_container_width=True):
            st.session_state.example_idea = "An AI-powered personal fitness coach app that creates personalized workout plans based on user goals, fitness level, and available equipment"
            st.rerun()
        
        if st.button("Sustainable fashion marketplace", use_container_width=True):
            st.session_state.example_idea = "A marketplace connecting eco-conscious consumers with sustainable fashion brands, featuring carbon footprint tracking"
            st.rerun()
        
        if st.button("B2B SaaS analytics", use_container_width=True):
            st.session_state.example_idea = "A B2B SaaS platform that provides real-time analytics and insights for small e-commerce businesses"
            st.rerun()
    
    # Main content area
    if missing_keys:
        st.info("👈 Please configure your API keys in the sidebar to get started")
        return
    
    st.markdown("### Enter Your Startup Idea")
    
    # Suggestion buttons at the top
    st.markdown("**Quick Examples:**")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("💪 AI Fitness Coach", use_container_width=True):
            st.session_state.example_idea = "An AI-powered personal fitness coach app that creates personalized workout plans based on user goals, fitness level, and available equipment. Uses computer vision to analyze form and provide real-time feedback during exercises."
            st.rerun()
    
    with col2:
        if st.button("🌱 Sustainable Fashion", use_container_width=True):
            st.session_state.example_idea = "A marketplace connecting eco-conscious consumers with sustainable fashion brands, featuring carbon footprint tracking for each purchase and personalized recommendations based on style preferences and sustainability values."
            st.rerun()
    
    st.markdown("")  # Add spacing
    
    # Check if example was selected and update the text area value in session state
    if "example_idea" in st.session_state:
        st.session_state.startup_idea_input = st.session_state.example_idea
        del st.session_state.example_idea
    
    startup_idea = st.text_area(
        "Describe your startup idea",
        height=150,
        key="startup_idea_input",
        placeholder="""Example: A marketplace for artisanal Christmas ornaments made from sustainable leather

Be specific about:
- What problem you're solving
- Who your target customers are
- How your solution is different
- What makes it unique""",
        help="Provide a clear description of your startup concept"
    )
    
    st.markdown("---")
    
    # Validate button
    col1, col2 = st.columns([3, 1])
    
    with col1:
        validate_button = st.button("Validate My Idea", type="primary", use_container_width=True)
    
    with col2:
        if st.session_state.results:
            if st.button("Clear Results", use_container_width=True):
                st.session_state.results = None
                st.rerun()
    
    if validate_button:
        if not startup_idea or not startup_idea.strip():
            st.error("Please enter a startup idea to validate")
            return
        
        # Store the idea in session state to preserve it during reruns
        st.session_state.current_idea = startup_idea.strip()
        
        # Process validation
        with st.spinner("Validating your startup idea... This may take a few minutes."):
            st.info("Running comprehensive analysis:\n\n"
                   "1. Clarifying and refining your idea...\n"
                   "2. Researching market size and opportunity...\n"
                   "3. Analyzing competitive landscape...\n"
                   "4. Generating validation report...")
            
            try:
                result = asyncio.run(validate_idea(
                    st.session_state.current_idea,
                    st.session_state.selected_model_id
                ))
                st.session_state.results = result
                st.success("Validation complete!")
                st.rerun()
            except Exception as e:
                st.error(f"Error during validation: {str(e)}")
                import traceback
                with st.expander("Show error details"):
                    st.code(traceback.format_exc())
    
    # Display results if available
    if st.session_state.results:
        st.markdown("---")
        display_results(st.session_state.results)


async def validate_idea(startup_idea: str, model_id: str = None):
    """Validate the startup idea and return results."""
    result = await validate_startup_idea(startup_idea, model_id=model_id)
    return result


if __name__ == "__main__":
    main()

