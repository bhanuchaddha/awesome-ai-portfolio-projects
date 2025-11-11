"""
Streamlit App for Blog Post Generator Agent

Run with: streamlit run streamlit_app.py
"""
import streamlit as st
from pathlib import Path
import sys
from importlib.util import spec_from_file_location, module_from_spec

# Get the root directory and add it to the Python path to enable imports
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

# Import the agent's functions
agent_module_name = "6_blog_post_generator_agent.6_blog_post_generator_agent"
agent_file_path = Path(__file__).resolve().parent / "6_blog_post_generator_agent.py"
spec = spec_from_file_location(agent_module_name, agent_file_path)
agent_module = module_from_spec(spec)
spec.loader.exec_module(agent_module)
generate_all_content = agent_module.generate_all_content

from common.streamlit_app_template import run_streamlit_app  # noqa: E402


async def get_agent_response(topic: str) -> str:
    """Get the agent's response with full content pipeline."""
    if not topic:
        return "## Error\n\n**Please provide a topic for the blog post.**"
    
    # Generate all content: research -> blog -> LinkedIn + Twitter
    result = await generate_all_content(topic)
    
    # Build formatted output with better UI
    output_parts = []
    
    # Check if blog post was generated
    if result["blog_post"] and not result["blog_post"].startswith("[ERROR]"):
        # Add the blog post
        output_parts.append(result["blog_post"])
        
        # Add social media section
        output_parts.append("\n\n---\n\n")
        output_parts.append("# Social Media Content\n\n")
        output_parts.append("Ready-to-post content for your social media channels.\n\n")
        
        # LinkedIn section
        if result["linkedin"] and not result["linkedin"].startswith("[ERROR]"):
            output_parts.append("## LinkedIn Post\n\n")
            output_parts.append("Copy and paste this into LinkedIn:\n\n")
            output_parts.append("```\n")
            output_parts.append(result["linkedin"])
            output_parts.append("\n```\n\n")
        
        # Twitter section
        if result["twitter"] and not result["twitter"].startswith("[ERROR]"):
            output_parts.append("## Twitter / X Thread\n\n")
            output_parts.append("Copy and paste this thread into Twitter/X:\n\n")
            output_parts.append("```\n")
            output_parts.append(result["twitter"])
            output_parts.append("\n```\n\n")
        
        # Research summary (collapsible)
        if result["research"]:
            output_parts.append("---\n\n")
            output_parts.append("<details>\n")
            output_parts.append("<summary><b>View Research Summary</b> (click to expand)</summary>\n\n")
            
            research = result["research"]
            output_parts.append(f"**Topic:** {research.topic}\n\n")
            
            if research.key_findings:
                output_parts.append("**Key Findings:**\n")
                for finding in research.key_findings:
                    output_parts.append(f"- {finding}\n")
                output_parts.append("\n")
            
            if research.main_themes:
                output_parts.append("**Main Themes:**\n")
                output_parts.append(f"{research.main_themes}\n\n")
            
            if research.important_statistics:
                output_parts.append("**Important Statistics:**\n")
                for stat in research.important_statistics:
                    output_parts.append(f"- {stat}\n")
                output_parts.append("\n")
            
            if research.expert_insights:
                output_parts.append("**Expert Insights:**\n")
                for insight in research.expert_insights:
                    output_parts.append(f"- {insight}\n")
                output_parts.append("\n")
            
            if research.sources:
                output_parts.append("**Sources:**\n")
                for i, source in enumerate(research.sources, 1):
                    if source.url:
                        output_parts.append(f"{i}. [{source.title}]({source.url})")
                    else:
                        output_parts.append(f"{i}. {source.title}")
                    if source.summary:
                        output_parts.append(f" - {source.summary}")
                    output_parts.append("\n")
            
            output_parts.append("\n</details>\n")
        
        return "".join(output_parts)
    else:
        # Show error message
        error_msg = result["blog_post"] if result["blog_post"] else "[ERROR] Content generation failed."
        return f"## Error\n\n**Content generation failed.**\n\n{error_msg}"


# Configure your agent's name and icon
AGENT_NAME = "Blog Post Generator"
AGENT_ICON = "B"
REQUIRED_SECRETS = ["EXA_API_KEY", "OPENROUTER_API_KEY"]

# Run the Streamlit app
run_streamlit_app(get_agent_response, AGENT_NAME, AGENT_ICON, REQUIRED_SECRETS)
