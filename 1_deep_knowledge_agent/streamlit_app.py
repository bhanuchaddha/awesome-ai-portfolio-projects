"""
Streamlit App for Deep Knowledge Agent

Run with: streamlit run streamlit_app.py
"""

import sys
from pathlib import Path
from importlib.util import spec_from_file_location, module_from_spec
import streamlit as st
from uuid import uuid4
from typing import Optional
import base64

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
from common.streamlit_app_template import (
    run_streamlit_app,
    _initialize_session_state,
    _display_sidebar,
    _display_chat_history,
    _handle_user_input,
)
from common.openrouter_utils import get_free_models

# 3. Configure your agent's name and icon
AGENT_NAME = "Deep Knowledge Agent"
AGENT_ICON = "📚"
REQUIRED_SECRETS = ["GOOGLE_API_KEY"]

# 4. Session management
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid4())

def get_response_with_session(message: str, file_path: Optional[str] = None) -> str:
    """Wrapper to pass session_id to the agent."""
    model_id = st.session_state.get("selected_model_id")
    return get_agent_response_func(
        message, st.session_state.session_id, file_path=file_path, model_id=model_id
    )


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

col_title, col_logo = st.columns([4, 1])
with col_title:
    st.title(f"{AGENT_ICON} {AGENT_NAME}")
with col_logo:
    if logo_path.exists():
        st.image(str(logo_path), width=120)

# Custom "How to use" section
sample_pdf_path = base_dir / "sample_input" / "elon_musk.pdf"
demo_gif_path = base_dir / "documentation" / "assets" / "demo.gif"

# Overview Section
st.markdown("---")
st.markdown(
    """
    ### What This Agent Does
    
    The **Deep Knowledge Agent** is an advanced AI-powered research assistant that performs **iterative searches** 
    through your documents to provide comprehensive, well-researched answers to complex questions. Unlike simple 
    question-answering systems, this agent:
    
    - **Breaks down complex queries** into manageable sub-questions
    - **Searches multiple times** to ensure no information is missed
    - **Synthesizes information** from different parts of your documents
    - **Provides source citations** for transparency and verification
    - **Documents its reasoning process** so you understand how it arrived at the answer
    
    **Perfect for:** Researchers, analysts, students, content creators, and anyone who needs deep insights from documents.
    """
)

# How it Works Section
with st.expander("How It Works - The Technology Behind the Agent", expanded=False):
    st.markdown(
        """
        ### The Deep Knowledge Process
        
        When you ask a question, the agent follows a systematic approach:
        
        1. **Query Analysis**: Breaks down your question into key components and identifies 3-5 search terms
        2. **Iterative Search**: Performs multiple searches (minimum 3) across the document knowledge base
        3. **Evaluation**: Assesses if the gathered information is complete and sufficient
        4. **Synthesis**: Combines information from multiple sources into a coherent answer
        5. **Citation**: Provides references to specific parts of the document
        
        ### Technology Stack
        
        This agent is built using cutting-edge AI technologies:
        
        | Component | Technology | Purpose |
        |-----------|-----------|---------|
        | **AI Framework** | Agno | Orchestrates the agent's behavior and reasoning |
        | **Language Model** | OpenRouter (MiniMax-M2) | Generates intelligent responses |
        | **Vector Database** | LanceDB | Stores and retrieves document embeddings |
        | **Embeddings** | Google Gemini Embedder | Converts text into searchable vectors |
        | **Document Processing** | Agentic Chunking | Intelligently splits documents for better retrieval |
        | **Search Type** | Hybrid Search | Combines semantic and keyword-based search |
        | **Memory** | SQLite | Maintains conversation history and context |
        
        ### Why This Approach Works
        
        - **Hybrid Search**: Combines semantic understanding with exact keyword matching for better accuracy
        - **Agentic Chunking**: Intelligently segments documents based on meaning, not just length
        - **Iterative Retrieval**: Multiple search passes ensure comprehensive coverage
        - **Context Memory**: Remembers previous conversations for better follow-up questions
        """
    )

# Quick Start Guide
with st.expander("Quick Start Guide - Get Started in 3 Steps", expanded=True):
    st.markdown(
        """
        ### Step 1: Configure API Key
        Enter your **Google API Key** in the sidebar. This is required for document embeddings.
        
        ### Step 2: Upload Your Document
        Upload a PDF file using the file uploader in the sidebar. You can:
        - Use your own PDF document, OR
        - Download our sample Elon Musk biography below to try it out
        
        ### Step 3: Ask Questions
        Start asking questions about your document! Try questions like:
        - "What are the main topics covered in this document?"
        - "Summarize the key achievements mentioned"
        - "What does the document say about [specific topic]?"
        
        The agent will search through the document multiple times to provide comprehensive answers with citations.
        """
    )
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### Watch the Demo")
        if demo_gif_path.exists():
            st.image(str(demo_gif_path), caption="See the agent in action", use_container_width=True)
        else:
            st.warning("Demo GIF not found.")
            
    with col2:
        st.markdown("#### Try with Sample Data")
        st.markdown("Download this sample PDF to test the agent immediately:")
        if sample_pdf_path.exists():
            with open(sample_pdf_path, "rb") as pdf_file:
                st.download_button(
                    label="Download Sample PDF (Elon Musk Biography)",
                    data=pdf_file,
                    file_name="elon_musk.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                )
            st.markdown(
                """
                **Sample Questions to Try:**
                - "What are Elon Musk's major companies?"
                - "Describe his early life and education"
                - "What are his views on artificial intelligence?"
                """
            )
        else:
            st.warning("Sample PDF not found.")

# Use Cases Section
with st.expander("Use Cases - Who Should Use This Agent?", expanded=False):
    st.markdown(
        """
        ### Research & Analysis
        - **Academic Research**: Quickly extract insights from research papers and literature
        - **Market Research**: Analyze reports and extract key findings
        - **Competitive Analysis**: Study competitor documents and whitepapers
        
        ### Content Creation
        - **Article Writing**: Research topics thoroughly before writing
        - **Report Generation**: Extract and synthesize information from multiple sources
        - **Presentation Prep**: Gather comprehensive information for presentations
        
        ### Learning & Education
        - **Study Aid**: Get detailed explanations from textbooks and course materials
        - **Literature Review**: Understand complex academic papers
        - **Exam Preparation**: Deep dive into study materials
        
        ### Business Intelligence
        - **Document Analysis**: Extract insights from contracts, proposals, and reports
        - **Due Diligence**: Thoroughly analyze business documents
        - **Knowledge Management**: Make organizational documents searchable and accessible
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
                # Default to a known good model if available, or the first one
                default_index = 0
                for i, name in enumerate(model_names):
                    if "minimax" in name.lower():
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

_display_sidebar(REQUIRED_SECRETS, enable_file_uploader=True)
_display_chat_history()
_handle_user_input(
    get_response_with_session,
    enable_file_uploader=True,
    required_secrets=REQUIRED_SECRETS,
)
