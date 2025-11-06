import asyncio
from textwrap import dedent

from agno.agent import Agent
from agno.tools.mcp import MCPTools
from agno.tools.reasoning import ReasoningTools
from agno.models.openrouter import OpenRouter
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()


def _create_agent(mcp_tools: MCPTools) -> Agent:
    """Create the competitor analysis agent."""
    return Agent(
        model=OpenRouter(id=os.getenv("OPENROUTER_MODEL_ID", "minimax/minimax-m2:free"), api_key=os.getenv("OPENROUTER_API_KEY")),
        tools=[
            ReasoningTools(
                add_instructions=True,
            ),
            mcp_tools,
        ],
        instructions=[
            "### Firecrawl Usage Guidelines:",
            "- **Search:** Use `firecrawl_search` for initial discovery. You MUST provide a `query` argument (e.g., `'[company name] competitors'`).",
            "- **Scrape:** Use `firecrawl_scrape` to get content from specific competitor websites.",
            "- **Map:** Use `firecrawl_map` to understand the structure of a competitor's website.",
            "",
            "### Research Workflow:",
            "1. **Initial Research & Discovery:**",
            "   - Use the search tool to find information about the target company, its competitors, and industry reports.",
            "   - Use the think tool to plan your research approach.",
            "2. **Competitor Identification:**",
            "   - For each potential competitor, use the search tool to find their official website.",
            "   - Map out the competitive landscape.",
            "3. **Website Analysis:**",
            "   - Scrape competitor websites to analyze their offerings.",
            "   - Map their site structure to understand their products, pricing, and value propositions.",
            "   - Look for case studies and customer testimonials.",
            "4. **Deep Competitive Analysis:**",
            "   - Use the analyze tool after gathering information on each competitor.",
            "   - Compare features, pricing, and market positioning.",
            "   - Identify patterns and competitive dynamics.",
            "   - Think through the implications of your findings.",
            "5. **Strategic Synthesis:**",
            "   - Conduct SWOT analysis for each major competitor.",
            "   - Use reasoning to identify competitive advantages.",
            "   - Analyze market trends and opportunities.",
            "   - Develop strategic recommendations.",
            "",
            "### General Guidelines:",
            "- Always use the `think` tool before starting major research phases.",
            "- Use the `analyze` tool to process findings and draw insights.",
            "- Search for multiple perspectives on each competitor and verify information by checking multiple sources.",
            "- Be thorough but focused in your analysis, providing evidence-based recommendations.",
        ],
        expected_output=dedent("""\
    # Competitive Analysis Report: {Target Company}

    ## Executive Summary
    {High-level overview of competitive landscape and key findings}

    ## Research Methodology
    - Search queries used
    - Websites analyzed
    - Key information sources

    ## Market Overview
    ### Industry Context
    - Market size and growth rate
    - Key trends and drivers
    - Regulatory environment

    ### Competitive Landscape
    - Major players identified
    - Market segmentation
    - Competitive dynamics

    ## Competitor Analysis

    ### Competitor 1: {Name}
    #### Company Overview
    - Website: {URL}
    - Founded: {Year}
    - Headquarters: {Location}
    - Company size: {Employees/Revenue if available}

    #### Products & Services
    - Core offerings
    - Key features and capabilities
    - Pricing model and tiers
    - Target market segments

    #### Digital Presence Analysis
    - Website structure and user experience
    - Key messaging and value propositions
    - Content strategy and resources
    - Customer proof points

    #### SWOT Analysis
    **Strengths:**
    - {Evidence-based strengths}

    **Weaknesses:**
    - {Identified weaknesses}

    **Opportunities:**
    - {Market opportunities}

    **Threats:**
    - {Competitive threats}

    ### Competitor 2: {Name}
    {Similar structure as above}

    ### Competitor 3: {Name}
    {Similar structure as above}

    ## Comparative Analysis

    ### Feature Comparison Matrix
    | Feature | {Target} | Competitor 1 | Competitor 2 | Competitor 3 |
    |---------|----------|--------------|--------------|--------------|
    | {Feature 1} | ✓/✗ | ✓/✗ | ✓/✗ | ✓/✗ |
    | {Feature 2} | ✓/✗ | ✓/✗ | ✓/✗ | ✓/✗ |

    ### Pricing Comparison
    | Company | Entry Level | Professional | Enterprise |
    |---------|-------------|--------------|------------|
    | {Pricing details extracted from websites} |

    ### Market Positioning Analysis
    {Analysis of how each competitor positions themselves}

    ## Strategic Insights

    ### Key Findings
    1. {Major insight with evidence}
    2. {Competitive dynamics observed}
    3. {Market gaps identified}

    ### Competitive Advantages
    - {Target company's advantages}
    - {Unique differentiators}

    ### Competitive Risks
    - {Main threats from competitors}
    - {Market challenges}

    ## Strategic Recommendations

    ### Immediate Actions (0-3 months)
    1. {Quick competitive responses}
    2. {Low-hanging fruit opportunities}

    ### Short-term Strategy (3-12 months)
    1. {Product/service enhancements}
    2. {Market positioning adjustments}

    ### Long-term Strategy (12+ months)
    1. {Sustainable differentiation}
    2. {Market expansion opportunities}

    ## Conclusion
    {Summary of competitive position and strategic imperatives}
    """),
        markdown=True,
        add_datetime_to_context=True,
        stream_events=True,
        debug_mode=True,
    )

async def get_agent_response(message: str) -> str:
    """Run agent and return response as string (for UI integration)."""
    firecrawl_api_key = os.getenv("FIRECRAWL_API_KEY")
    if not firecrawl_api_key:
        raise ValueError("FIRECRAWL_API_KEY environment variable not set")
    mcp_tools = MCPTools(
        url=f"https://mcp.firecrawl.dev/{firecrawl_api_key}/v2/mcp",
        transport="streamable-http",
    )
    await mcp_tools.connect()

    try:
        agent = _create_agent(mcp_tools)
        
        # The `arun` method returns a `RunOutput` object.
        # The final response is in the `output` attribute.
        run_output = await agent.arun(message)
        response = run_output.content

        return response if isinstance(response, str) else str(response)
    finally:
        await mcp_tools.close()


async def run_agent(message: str) -> None:
    # Use .connect()/.close() style, not async context manager
    firecrawl_api_key = os.getenv("FIRECRAWL_API_KEY")
    if not firecrawl_api_key:
        raise ValueError("FIRECRAWL_API_KEY environment variable not set")
    mcp_tools = MCPTools(
        url=f"https://mcp.firecrawl.dev/{firecrawl_api_key}/v2/mcp",
        transport="streamable-http",
    )
    await mcp_tools.connect()

    try:
        competitor_analysis_agent = _create_agent(mcp_tools)
        await competitor_analysis_agent.aprint_response(
            message,
            stream=True,
            show_full_reasoning=True,
        )
    finally:
        await mcp_tools.close()

if __name__ == "__main__":
    task = """Analyze the competitive landscape for Novo Nordisk in the pharmaceutical industry.
    """
    asyncio.run(run_agent(task))