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

async def run_agent(message: str) -> None:
    # Use .connect()/.close() style, not async context manager
    mcp_tools = MCPTools(command="npx -y @openbnb/mcp-server-airbnb --ignore-robots-txt")
    await mcp_tools.connect()

    try:
        agent = Agent(
            model=OpenRouter(id=os.getenv("OPENROUTER_MODEL_ID"), api_key=os.getenv("OPENROUTER_API_KEY")),
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
        await agent.aprint_response(message, stream=True)
    finally:
        await mcp_tools.close()

if __name__ == "__main__":
    task = dedent("""
    I'm traveling to Copenhagen from Jan 1st - Jan 8th. Can you find me the best deals for a 1 bedroom apartment?
    I'd like a dedicated workspace and close proximity to Trivoli.
    """)
    asyncio.run(run_agent(task))
