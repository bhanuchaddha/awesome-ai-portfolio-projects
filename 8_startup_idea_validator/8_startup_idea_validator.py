"""Startup Idea Validator - Your AI Business Validation Assistant!

An automated system that helps entrepreneurs validate their startup ideas through:
- Idea clarification and refinement
- Comprehensive market research
- Competitive landscape analysis
- Strategic recommendations

Features:
- Multi-agent validation pipeline
- Web research with Exa
- Market opportunity analysis
- Competitive positioning assessment
- Actionable next steps
"""

import os
from textwrap import dedent
from typing import Any, Optional

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openrouter import OpenRouter
from agno.tools.exa import ExaTools
from agno.utils.log import logger
from agno.workflow.types import WorkflowExecutionInput
from agno.workflow.workflow import Workflow
from dotenv import load_dotenv
from pydantic import BaseModel, Field

# Load environment variables
load_dotenv()


# --- Helper function to safely initialize tools ---
def get_tools():
    """Return Exa tools if API key is available, otherwise empty list."""
    try:
        return [ExaTools(show_results=True)] if os.getenv("EXA_API_KEY") else []
    except:
        return []


# --- Pydantic Models ---

class IdeaClarification(BaseModel):
    """Results from idea clarification phase."""
    originality: str = Field(..., description="Originality of the idea compared to existing solutions")
    mission: str = Field(..., description="Mission statement of the company")
    objectives: str = Field(..., description="Specific measurable objectives of the company")


class MarketResearch(BaseModel):
    """Results from market research phase."""
    total_addressable_market: str = Field(..., description="Total addressable market (TAM) analysis")
    serviceable_available_market: str = Field(..., description="Serviceable available market (SAM) analysis")
    serviceable_obtainable_market: str = Field(..., description="Serviceable obtainable market (SOM) analysis")
    target_customer_segments: str = Field(..., description="Detailed target customer segments")


class CompetitorAnalysis(BaseModel):
    """Results from competitor analysis phase."""
    competitors: str = Field(..., description="List of identified direct and indirect competitors")
    swot_analysis: str = Field(..., description="SWOT analysis for each major competitor")
    positioning: str = Field(..., description="Startup's potential positioning relative to competitors")


class ValidationReport(BaseModel):
    """Final comprehensive validation report."""
    executive_summary: str = Field(..., description="Executive summary of the validation")
    idea_assessment: str = Field(..., description="Assessment of the startup idea strengths and weaknesses")
    market_opportunity: str = Field(..., description="Market opportunity analysis")
    competitive_landscape: str = Field(..., description="Competitive landscape overview")
    recommendations: str = Field(..., description="Strategic recommendations")
    next_steps: str = Field(..., description="Specific recommended next steps")


# --- Agents ---

idea_clarifier_agent = Agent(
    name="Idea Clarifier",
    model=OpenRouter(
        id=os.getenv("OPENROUTER_MODEL_ID", "minimax/minimax-m2:free"),
        api_key=os.getenv("OPENROUTER_API_KEY")
    ),
    description=dedent("""\
    You are an expert startup advisor who helps refine and clarify business ideas.
    You evaluate originality, define mission, and set clear objectives.
    """),
    instructions=dedent("""\
    Given a startup idea, refine and clarify it:
    
    1. Evaluate Originality:
       - Compare with existing solutions
       - Identify unique value proposition
       - Assess innovation level
       - Note market gaps being addressed
    
    2. Define Mission:
       - Create clear, inspiring mission statement
       - Focus on problem being solved
       - Include target audience
       - Keep it concise and memorable
    
    3. Set Objectives:
       - List 3-5 specific, measurable objectives
       - Make them SMART (Specific, Measurable, Achievable, Relevant, Time-bound)
       - Focus on key success metrics
       - Align with mission
    
    Provide constructive, actionable insights to strengthen the concept.
    """),
    output_schema=IdeaClarification,
    markdown=True,
    debug_mode=True,
)

market_research_agent = Agent(
    name="Market Research Agent",
    model=OpenRouter(
        id=os.getenv("OPENROUTER_MODEL_ID", "minimax/minimax-m2:free"),
        api_key=os.getenv("OPENROUTER_API_KEY")
    ),
    tools=get_tools(),
    description=dedent("""\
    You are a market research expert who analyzes market size, segments, and opportunities.
    You use web research to find data and provide realistic market estimates.
    """),
    instructions=dedent("""\
    You have access to the search_exa tool. YOU MUST USE IT - don't just write about using it.
    
    CRITICAL: Do NOT write "search_exa(query='...')" as text. Actually CALL the tool.
    When you see tools available, USE THEM by calling them, not by writing their names.
    
    STEP 1: EXECUTE searches (the tool will be called automatically, just specify what to search):
    Start by researching:
    - Market size for the industry
    - Target customer demographics  
    - Market trends
    - Consumer segments
    
    Search for relevant information using your available tools.
    
    STEP 2: After getting search results, provide a comprehensive report with:
    
    1. Total Addressable Market (TAM):
       - Overall market size with dollar estimates
       - Growth projections
       - Cite sources from search results
    
    2. Serviceable Available Market (SAM):
       - Realistic portion of market you can serve
       - Geographic and demographic constraints
       - Business model considerations
    
    3. Serviceable Obtainable Market (SOM):
       - Realistic market share (1-5 years)
       - Competition and resource constraints
       - Conservative estimates
    
    4. Target Customer Segments:
       - 2-4 primary customer segments
       - Demographics, psychographics
       - Pain points and needs
       - Segment sizes
    
    Format your response with clear sections:
    ### TOTAL ADDRESSABLE MARKET (TAM)
    [Your analysis here]
    
    ### SERVICEABLE AVAILABLE MARKET (SAM)
    [Your analysis here]
    
    ### SERVICEABLE OBTAINABLE MARKET (SOM)
    [Your analysis here]
    
    ### TARGET CUSTOMER SEGMENTS
    [Your analysis here]
    
    If searches fail or data is insufficient, state "Data not available" for that section.
    """),
    markdown=True,
    debug_mode=True,
)

competitor_analysis_agent = Agent(
    name="Competitor Analysis Agent",
    model=OpenRouter(
        id=os.getenv("OPENROUTER_MODEL_ID", "minimax/minimax-m2:free"),
        api_key=os.getenv("OPENROUTER_API_KEY")
    ),
    tools=get_tools(),
    description=dedent("""\
    You are a competitive intelligence analyst who identifies competitors
    and analyzes market positioning.
    """),
    instructions=dedent("""\
    You have access to the search_exa tool. YOU MUST USE IT - don't just write about using it.
    
    CRITICAL: Do NOT write "search_exa(query='...')" as text. Actually CALL the tool.
    When you see tools available, USE THEM by calling them, not by writing their names.
    
    STEP 1: EXECUTE searches (the tool will be called automatically):
    Research information about:
    - Competitors in the space
    - Market leaders
    - Companies in the industry
    - Relevant startups
    
    Use your available tools to find this information.
    
    STEP 2: After getting search results, provide a comprehensive analysis with:
    
    1. Identified Competitors:
       - 5-10 direct competitors
       - 3-5 indirect competitors
       - Include startups and established companies
       - Brief description of each
    
    2. SWOT Analysis:
       - Analyze major competitors
       - Strengths, Weaknesses, Opportunities, Threats
       - Differentiation points
       - Market positioning
    
    3. Competitive Positioning:
       - Assess startup's potential position
       - Market gaps and opportunities
       - Differentiation strategy
       - Competitive advantages
    
    4. Market Dynamics:
       - Industry trends
       - Barriers to entry
       - Competitive intensity
    
    Format your response with clear sections:
    ### IDENTIFIED COMPETITORS
    [Your analysis here]
    
    ### SWOT ANALYSIS
    [Your analysis here]
    
    ### COMPETITIVE POSITIONING
    [Your analysis here]
    
    If searches fail or data is insufficient, state "Data not available" for that section.
    """),
    markdown=True,
    debug_mode=True,
)

report_agent = Agent(
    name="Report Generator",
    model=OpenRouter(
        id=os.getenv("OPENROUTER_MODEL_ID", "minimax/minimax-m2:free"),
        api_key=os.getenv("OPENROUTER_API_KEY")
    ),
    description=dedent("""\
    You are a business analyst who synthesizes research into comprehensive,
    actionable validation reports.
    """),
    instructions=dedent("""\
    Create a comprehensive startup validation report:
    
    1. Executive Summary:
       - High-level overview (2-3 paragraphs)
       - Key findings and recommendation
       - Go/No-Go assessment
    
    2. Idea Assessment:
       - Evaluate concept strength
       - Identify key strengths
       - Note concerns or weaknesses
       - Assess market fit
    
    3. Market Opportunity:
       - Summarize TAM/SAM/SOM
       - Describe target segments
       - Evaluate market attractiveness
       - Note growth potential
    
    4. Competitive Landscape:
       - Summarize competitor analysis
       - Assess competitive intensity
       - Identify differentiation opportunities
       - Note barriers to entry
    
    5. Strategic Recommendations:
       - Provide 3-5 specific recommendations
       - Focus on actionable insights
       - Prioritize by importance
       - Address key risks
    
    6. Next Steps:
       - List specific actions
       - Suggest validation experiments
       - Recommend resources needed
       - Set milestones
    
    Make the report professional, clear, and actionable.
    """),
    output_schema=ValidationReport,
    markdown=True,
    debug_mode=True,
)


# --- Workflow Execution Function ---

async def startup_validation_execution(
    workflow: Workflow,
    execution_input: WorkflowExecutionInput,
    **kwargs: Any,
) -> dict:
    """Execute the complete startup idea validation workflow"""
    
    # Get inputs
    message: str = execution_input.input
    idea: str = kwargs.get("startup_idea", "")
    model_id: str = kwargs.get("model_id") or os.getenv("OPENROUTER_MODEL_ID", "minimax/minimax-m2:free")
    
    if not idea:
        return {
            "error": "No startup idea provided",
            "idea_clarification": None,
            "market_research": None,
            "competitor_analysis": None,
            "validation_report": None
        }
    
    # Validate required API keys
    if not os.getenv("EXA_API_KEY"):
        return {
            "error": "EXA_API_KEY is required for startup validation. This agent uses web search to gather market research and competitive intelligence. Please provide your EXA_API_KEY in the sidebar configuration.",
            "idea_clarification": None,
            "market_research": None,
            "competitor_analysis": None,
            "validation_report": None
        }
    
    print(f"[START] Starting startup idea validation for: {idea[:100]}...")
    print(f"[INFO] Validation request: {message}")
    print(f"[INFO] Using model: {model_id}")
    logger.info("=" * 60)
    logger.info(f"[CONFIG] Model: {model_id}")
    
    # Create agents with the selected model
    current_idea_clarifier = Agent(
        name="Idea Clarifier",
        model=OpenRouter(
            id=model_id,
            api_key=os.getenv("OPENROUTER_API_KEY")
        ),
        description=idea_clarifier_agent.description,
        instructions=idea_clarifier_agent.instructions,
        output_schema=IdeaClarification,
        markdown=True,
        debug_mode=True,
    )
    
    current_market_research = Agent(
        name="Market Research Agent",
        model=OpenRouter(
            id=model_id,
            api_key=os.getenv("OPENROUTER_API_KEY")
        ),
        tools=get_tools(),
        description=market_research_agent.description,
        instructions=market_research_agent.instructions,
        markdown=True,
        debug_mode=True,
    )
    
    current_competitor_analysis = Agent(
        name="Competitor Analysis Agent",
        model=OpenRouter(
            id=model_id,
            api_key=os.getenv("OPENROUTER_API_KEY")
        ),
        tools=get_tools(),
        description=competitor_analysis_agent.description,
        instructions=competitor_analysis_agent.instructions,
        markdown=True,
        debug_mode=True,
    )
    
    current_report_agent = Agent(
        name="Report Generator",
        model=OpenRouter(
            id=model_id,
            api_key=os.getenv("OPENROUTER_API_KEY")
        ),
        description=report_agent.description,
        instructions=report_agent.instructions,
        output_schema=ValidationReport,
        markdown=True,
        debug_mode=True,
    )
    
    # Phase 1: Idea Clarification
    print("\n[PHASE 1] IDEA CLARIFICATION & REFINEMENT")
    print("=" * 60)
    logger.info("[PHASE 1] IDEA CLARIFICATION & REFINEMENT")
    logger.info("-" * 60)
    
    clarification_prompt = f"""
    {message}

    Please analyze and refine the following startup idea:

    STARTUP IDEA: {idea}

    Evaluate:
    1. The originality of this idea compared to existing solutions
    2. Define a clear mission statement for this startup
    3. Outline specific, measurable objectives

    Provide insights on how to strengthen and focus the core concept.
    """
    
    print("[INFO] Analyzing and refining the startup concept...")
    
    response = await current_idea_clarifier.arun(clarification_prompt)
    
    if not isinstance(response.content, IdeaClarification):
        logger.warning(f"[WARNING] Model returned unstructured output, using text response")
        text_content = str(response.content)
        
        # Clean up text content - remove raw search queries if present
        if "search_exa" in text_content or "query=" in text_content:
            text_content = "Data not available"
        
        idea_clarification = IdeaClarification(
            originality=text_content[:500] if text_content and len(text_content) > 30 else "Data not available - idea requires detailed analysis",
            mission="Data not available - mission to be refined based on detailed analysis",
            objectives="1. Validate market demand\n2. Build MVP\n3. Acquire initial customers"
        )
        print("[WARNING] Idea clarification completed (unstructured response)")
    else:
        idea_clarification = response.content
        print("[SUCCESS] Idea clarification completed")
    
    print(f"[INFO] Mission: {idea_clarification.mission[:100]}...")
    logger.info(f"[SUCCESS] Idea clarification complete")
    
    # Phase 2: Market Research
    print("\n[PHASE 2] MARKET RESEARCH & ANALYSIS")
    print("=" * 60)
    logger.info("\n[PHASE 2] MARKET RESEARCH & ANALYSIS")
    logger.info("-" * 60)
    
    market_prompt = f"""
    Based on the refined startup idea and clarification below, conduct comprehensive market research:

    STARTUP IDEA: {idea}
    ORIGINALITY: {idea_clarification.originality}
    MISSION: {idea_clarification.mission}
    OBJECTIVES: {idea_clarification.objectives}

    Please research and provide:
    1. Total Addressable Market (TAM) - overall market size
    2. Serviceable Available Market (SAM) - portion you could serve
    3. Serviceable Obtainable Market (SOM) - realistic market share
    4. Target customer segments with detailed characteristics

    Use Exa search to find current market data and trends.
    """
    
    print("[INFO] Researching market size and customer segments...")
    
    response = await current_market_research.arun(market_prompt)
    text_content = str(response.content)
    
    # Parse the response to extract sections
    def extract_section(text, markers):
        """Extract content between section markers."""
        for marker in markers:
            if marker.upper() in text.upper():
                # Find the start of this section
                start_idx = text.upper().find(marker.upper())
                # Find the start of the next section (if any)
                remaining_text = text[start_idx + len(marker):]
                # Look for next section marker
                next_markers = ["### TOTAL ADDRESSABLE", "### SERVICEABLE AVAILABLE", 
                              "### SERVICEABLE OBTAINABLE", "### TARGET CUSTOMER"]
                end_idx = len(remaining_text)
                for next_marker in next_markers:
                    pos = remaining_text.upper().find(next_marker.upper())
                    if pos > 0 and pos < end_idx:
                        end_idx = pos
                return remaining_text[:end_idx].strip()
        return "Data not available"
    
    # Check if response contains tool calls as text (not executed)
    if "search_exa(query=" in text_content:
        logger.warning("[WARNING] Model output contains unexecuted search queries - model described searches instead of executing them")
        # Try to clean up the response by removing the search query lines
        lines = text_content.split('\n')
        cleaned_lines = []
        for line in lines:
            # Skip lines that are just search query descriptions
            if 'search_exa(query=' not in line and '[search_exa' not in line and 'To identify' not in line:
                cleaned_lines.append(line)
        text_content = '\n'.join(cleaned_lines).strip()
        
        # If there's no useful content left after cleaning, use a default message
        if len(text_content) < 100:
            logger.warning("[WARNING] No useful market research content found after cleaning")
            text_content = "Market research could not be completed. The selected AI model has limited tool-calling capabilities and did not execute web searches. Try using a more capable model (e.g., one of the non-free models) for better results with web research."
    
    # Extract structured information from the response
    tam = extract_section(text_content, ["### TOTAL ADDRESSABLE MARKET", "TAM:", "Total Addressable Market"])
    sam = extract_section(text_content, ["### SERVICEABLE AVAILABLE MARKET", "SAM:", "Serviceable Available Market"])
    som = extract_section(text_content, ["### SERVICEABLE OBTAINABLE MARKET", "SOM:", "Serviceable Obtainable Market"])
    segments = extract_section(text_content, ["### TARGET CUSTOMER SEGMENTS", "Target Customer Segments", "Customer Segments"])
    
    # If sections are too short, use the full response
    if len(tam) < 50:
        tam = text_content[:1000] if len(text_content) > 50 else "Data not available - market size requires detailed analysis"
    if len(sam) < 20:
        sam = "Data not available - target market segment to be determined through research"
    if len(som) < 20:
        som = "Data not available - realistic market share to be calculated"
    if len(segments) < 20:
        segments = "Data not available - customer segments to be defined through market research"
    
    market_research = MarketResearch(
        total_addressable_market=tam,
        serviceable_available_market=sam,
        serviceable_obtainable_market=som,
        target_customer_segments=segments
    )
    print("[SUCCESS] Market research completed")
    
    print(f"[INFO] TAM: {market_research.total_addressable_market[:100]}...")
    logger.info(f"[SUCCESS] Market research complete")
    
    # Phase 3: Competitor Analysis
    print("\n[PHASE 3] COMPETITIVE LANDSCAPE ANALYSIS")
    print("=" * 60)
    logger.info("\n[PHASE 3] COMPETITIVE LANDSCAPE ANALYSIS")
    logger.info("-" * 60)
    
    competitor_prompt = f"""
    Based on the startup idea and market research below, analyze the competitive landscape:

    STARTUP IDEA: {idea}
    TAM: {market_research.total_addressable_market}
    SAM: {market_research.serviceable_available_market}
    SOM: {market_research.serviceable_obtainable_market}
    TARGET SEGMENTS: {market_research.target_customer_segments}

    Please research and provide:
    1. Identify direct and indirect competitors
    2. SWOT analysis for each major competitor
    3. Assessment of startup's potential competitive positioning
    4. Market gaps and opportunities

    Use Exa search to find current competitor information.
    """
    
    print("[INFO] Analyzing competitive landscape...")
    
    response = await current_competitor_analysis.arun(competitor_prompt)
    text_content = str(response.content)
    
    # Parse the response to extract sections
    def extract_competitor_section(text, markers):
        """Extract content between section markers."""
        for marker in markers:
            if marker.upper() in text.upper():
                start_idx = text.upper().find(marker.upper())
                remaining_text = text[start_idx + len(marker):]
                next_markers = ["### IDENTIFIED COMPETITORS", "### SWOT ANALYSIS", "### COMPETITIVE POSITIONING"]
                end_idx = len(remaining_text)
                for next_marker in next_markers:
                    pos = remaining_text.upper().find(next_marker.upper())
                    if pos > 0 and pos < end_idx:
                        end_idx = pos
                return remaining_text[:end_idx].strip()
        return "Data not available"
    
    # Check if response contains tool calls as text (not executed)
    if "search_exa(query=" in text_content:
        logger.warning("[WARNING] Model output contains unexecuted search queries - model described searches instead of executing them")
        # Try to clean up the response by removing the search query lines
        lines = text_content.split('\n')
        cleaned_lines = []
        for line in lines:
            # Skip lines that are just search query descriptions
            if 'search_exa(query=' not in line and '[search_exa' not in line and 'To identify' not in line and 'we need to execute' not in line:
                cleaned_lines.append(line)
        text_content = '\n'.join(cleaned_lines).strip()
        
        # If there's no useful content left after cleaning, use a default message  
        if len(text_content) < 100:
            logger.warning("[WARNING] No useful competitor analysis content found after cleaning")
            text_content = "Competitor analysis could not be completed. The selected AI model has limited tool-calling capabilities and did not execute web searches. Try using a more capable model (e.g., one of the non-free models) for better results with web research."
    
    # Extract structured information from the response
    competitors = extract_competitor_section(text_content, ["### IDENTIFIED COMPETITORS", "Identified Competitors:", "Competitors:"])
    swot = extract_competitor_section(text_content, ["### SWOT ANALYSIS", "SWOT Analysis:", "SWOT:"])
    positioning = extract_competitor_section(text_content, ["### COMPETITIVE POSITIONING", "Competitive Positioning:", "Positioning:"])
    
    # If sections are too short, use the full response or default
    if len(competitors) < 50:
        competitors = text_content[:1000] if len(text_content) > 50 else "Data not available - competitive landscape requires detailed market analysis"
    if len(swot) < 20:
        swot = "Data not available - SWOT analysis to be conducted for key competitors"
    if len(positioning) < 20:
        positioning = "Data not available - market positioning strategy to be developed"
    
    competitor_analysis = CompetitorAnalysis(
        competitors=competitors,
        swot_analysis=swot,
        positioning=positioning
    )
    print("[SUCCESS] Competitor analysis completed")
    
    print(f"[INFO] Positioning: {competitor_analysis.positioning[:100]}...")
    logger.info(f"[SUCCESS] Competitor analysis complete")
    
    # Phase 4: Final Validation Report
    print("\n[PHASE 4] COMPREHENSIVE VALIDATION REPORT")
    print("=" * 60)
    logger.info("\n[PHASE 4] COMPREHENSIVE VALIDATION REPORT")
    logger.info("-" * 60)
    
    report_prompt = f"""
    Synthesize all the research and analysis into a comprehensive startup validation report:

    STARTUP IDEA: {idea}

    IDEA CLARIFICATION:
    - Originality: {idea_clarification.originality}
    - Mission: {idea_clarification.mission}
    - Objectives: {idea_clarification.objectives}

    MARKET RESEARCH:
    - TAM: {market_research.total_addressable_market}
    - SAM: {market_research.serviceable_available_market}
    - SOM: {market_research.serviceable_obtainable_market}
    - Target Segments: {market_research.target_customer_segments}

    COMPETITOR ANALYSIS:
    - Competitors: {competitor_analysis.competitors}
    - SWOT: {competitor_analysis.swot_analysis}
    - Positioning: {competitor_analysis.positioning}

    Create a professional validation report with:
    1. Executive summary
    2. Idea assessment (strengths/weaknesses)
    3. Market opportunity analysis
    4. Competitive landscape overview
    5. Strategic recommendations
    6. Specific next steps for the entrepreneur
    """
    
    print("[INFO] Generating comprehensive validation report...")
    
    response = await current_report_agent.arun(report_prompt)
    
    if not isinstance(response.content, ValidationReport):
        logger.warning(f"[WARNING] Model returned unstructured output, using text response")
        text_content = str(response.content)
        
        # Clean up text content - remove raw search queries if present
        if "search_exa" in text_content or "query=" in text_content:
            text_content = "Data not available - validation report could not be fully generated"
        
        validation_report = ValidationReport(
            executive_summary=text_content[:600] if text_content and len(text_content) > 50 else "Data not available - startup validation completed with limited data",
            idea_assessment="Data not available - the concept requires further validation through customer discovery and market testing",
            market_opportunity="Data not available - market opportunity exists but requires detailed research and validation",
            competitive_landscape="Data not available - competitive analysis indicates opportunities for differentiation",
            recommendations="1. Validate assumptions with target customers\n2. Research market size and competition\n3. Build MVP to test core value proposition",
            next_steps="1. Conduct customer discovery interviews\n2. Analyze competitive positioning\n3. Develop go-to-market strategy"
        )
        print("[WARNING] Validation report completed (unstructured response)")
    else:
        validation_report = response.content
        print("[SUCCESS] Validation report completed")
    
    logger.info(f"[SUCCESS] Validation report complete")
    
    print("\n[COMPLETE] STARTUP IDEA VALIDATION COMPLETED!")
    logger.info("=" * 60)
    logger.info("[COMPLETE] Startup idea validation finished")
    
    # Convert Pydantic models to dicts for JSON serialization
    return {
        "idea_clarification": idea_clarification.model_dump() if hasattr(idea_clarification, 'model_dump') else idea_clarification,
        "market_research": market_research.model_dump() if hasattr(market_research, 'model_dump') else market_research,
        "competitor_analysis": competitor_analysis.model_dump() if hasattr(competitor_analysis, 'model_dump') else competitor_analysis,
        "validation_report": validation_report.model_dump() if hasattr(validation_report, 'model_dump') else validation_report
    }


# --- Workflow Definition ---

startup_validation_workflow = Workflow(
    name="Startup Idea Validator",
    description="Comprehensive startup idea validation with market research and competitive analysis",
    db=SqliteDb(
        session_table="workflow_session",
        db_file="tmp/workflows.db",
    ),
    steps=startup_validation_execution,
    session_state={},  # Initialize empty workflow session state
)


# --- Helper Function for External Use ---

async def validate_startup_idea(startup_idea: str, model_id: str = None) -> dict:
    """
    Validate a startup idea through comprehensive analysis.
    
    This is a convenience wrapper around the workflow for direct usage.
    
    Args:
        startup_idea: The startup idea to validate
        model_id: Optional OpenRouter model ID to use (defaults to env var or minimax)
    
    Returns a dictionary with:
    - idea_clarification: Refined concept analysis
    - market_research: Market size and segments
    - competitor_analysis: Competitive landscape
    - validation_report: Final comprehensive report
    """
    result = await startup_validation_workflow.arun(
        input="Please validate this startup idea with comprehensive market research and competitive analysis",
        startup_idea=startup_idea,
        model_id=model_id,
    )
    
    return result.content if hasattr(result, 'content') else result

