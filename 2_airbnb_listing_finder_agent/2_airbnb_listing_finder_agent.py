import asyncio
from textwrap import dedent
from agno.agent import Agent
import io
import sys

from agno.tools.mcp import MCPTools
from agno.tools.reasoning import ReasoningTools


from agno.models.openrouter import OpenRouter
from dotenv import load_dotenv
import os

from typing import Optional

# Load environment variables from .env file
load_dotenv()

def _create_agent(mcp_tools, model_id: Optional[str] = None):
    """Helper function to create agent with shared configuration."""
    final_model_id = model_id or os.getenv("OPENROUTER_MODEL_ID", "meta-llama/llama-4-maverick:free")
    return Agent(
        model=OpenRouter(id=final_model_id, api_key=os.getenv("OPENROUTER_API_KEY")),
        tools=[ReasoningTools(add_instructions=True), mcp_tools],
        instructions=dedent("""
        ## General Instructions
        - Always start by using the think tool to map out the steps needed to complete the task.
        - After receiving tool results, use the think tool as a scratchpad to validate the results for correctness
        - Before responding to the user, use the think tool to jot down final thoughts and ideas.
        - Present final outputs in well-organized tables whenever possible.
        - Always provide links to the listings in your response.
        - Show your top 10 recommendations in a table and make a case for why each is the best choice.

        ## Using the think tool
        At every step, use the think tool as a scratchpad to:
        - Restate the object in your own words to ensure full comprehension.
        - List the specific rules that apply to the current request
        - Check if all required information is collected and is valid
        - Verify that the planned action completes the task
        """),
        add_datetime_to_context=True,
        markdown=True,
    )

async def run_agent(message: str) -> None:
    """Run agent and print response to stdout (for standalone CLI use)."""
    # Use .connect()/.close() style, not async context manager
    
    airbnb_api_key = os.getenv("AIRBNB_MCP_API_KEY")
    airbnb_profile = os.getenv("AIRBNB_MCP_PROFILE")
    
    if not airbnb_api_key or not airbnb_profile:
        print("Error: AIRBNB_MCP_API_KEY and AIRBNB_MCP_PROFILE environment variables are required.")
        return

    mcp_url = f"https://server.smithery.ai/@iclickfreedownloads/mcp-server-airbnb/mcp?api_key={airbnb_api_key}&profile={airbnb_profile}"

    mcp_tools = MCPTools(
        url=mcp_url,
        transport="streamable-http"
    )
    await mcp_tools.connect()

    try:
        agent = _create_agent(mcp_tools)
        await agent.aprint_response(message, stream=True)
    finally:
        await mcp_tools.close()

async def get_agent_response(message: str, model_id: Optional[str] = None) -> str:
    """Run agent and return response as string (for UI integration)."""
    # Use .connect()/.close() style, not async context manager
    
    airbnb_api_key = os.getenv("AIRBNB_MCP_API_KEY")
    airbnb_profile = os.getenv("AIRBNB_MCP_PROFILE")
    
    if not airbnb_api_key or not airbnb_profile:
        return "Error: AIRBNB_MCP_API_KEY and AIRBNB_MCP_PROFILE environment variables are not set. Please configure them in the sidebar."

    mcp_url = f"https://server.smithery.ai/@iclickfreedownloads/mcp-server-airbnb/mcp?api_key={airbnb_api_key}&profile={airbnb_profile}"
    
    mcp_tools = MCPTools(
        url=mcp_url,
        transport="streamable-http"
    )
    await mcp_tools.connect()

    try:
        agent = _create_agent(mcp_tools, model_id=model_id)

        run_output = await agent.arun(message)
        response = run_output.content

        return response 
    finally:
        await mcp_tools.close()

if __name__ == "__main__":
    task = dedent("""
    I'm traveling to Copenhagen from Jan 1st - Jan 8th. Can you find me the best deals for a 1 bedroom apartment?
    I'd like a dedicated workspace and close proximity to Trivoli.
    """)
    asyncio.run(run_agent(task))
