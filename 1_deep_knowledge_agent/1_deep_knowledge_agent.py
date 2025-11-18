from textwrap import dedent
from typing import Optional

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.knowledge.embedder.openai import OpenAIEmbedder
from agno.knowledge.embedder.google import GeminiEmbedder
from agno.knowledge.reader.pdf_reader import PDFReader
from agno.knowledge.knowledge import Knowledge
from agno.models.openai import OpenAIChat
from agno.vectordb.lancedb import LanceDb, SearchType
from agno.knowledge.chunking.agentic import AgenticChunking

from agno.models.openrouter import OpenRouter
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()


def initialize_knowledge_base(file_path: Optional[str] = None):
    """Initialize the knowledge base with Agno docs."""
    agent_knowledge = Knowledge(
        vector_db=LanceDb(
            uri="tmp/lancedb",
            table_name="deep_knowledge_knowledge",
            search_type=SearchType.hybrid,
            embedder=GeminiEmbedder(),
        ),
    )
    # This might take a moment the first time it runs
    if file_path:
        agent_knowledge.add_content(
            path=file_path,
            reader=PDFReader(
                name="Document Chunking Reader",
                chunking_strategy=AgenticChunking(),
            ),
        )
    return agent_knowledge


def get_agent_db():
    """Return agent storage."""
    return SqliteDb(session_table="deep_knowledge_sessions", db_file="tmp/agents.db")


def create_agent(
    session_id: Optional[str] = None, 
    file_path: Optional[str] = None,
    model_id: Optional[str] = None
) -> Agent:
    """Create and return a configured DeepKnowledge agent."""
    agent_knowledge = initialize_knowledge_base(file_path=file_path)
    agent_db = get_agent_db()
    
    # Determine the model ID to use
    final_model_id = model_id or os.getenv("OPENROUTER_MODEL_ID", "minimax/minimax-m2:free")
    
    return Agent(
        name="DeepKnowledge",
        session_id=session_id,
        model=OpenRouter(id=final_model_id, api_key=os.getenv("OPENROUTER_API_KEY")),
        description=dedent("""\
        You are DeepKnowledge, an advanced reasoning agent designed to provide thorough,
        well-researched answers to any query by searching your knowledge base.

        Your strengths include:
        - Breaking down complex topics into manageable components
        - Connecting information across multiple domains
        - Providing nuanced, well-researched answers
        - Maintaining intellectual honesty and citing sources
        - Explaining complex concepts in clear, accessible terms"""),
        instructions=dedent("""\
        Your mission is to leave no stone unturned in your pursuit of the correct answer.

        To achieve this, follow these steps:
        1. **Analyze the input and break it down into key components**.
        2. **Search terms**: You must identify at least 3-5 key search terms to search for.
        3. **Initial Search:** Searching your knowledge base for relevant information. You must make atleast 3 searches to get all relevant information.
        4. **Evaluation:** If the answer from the knowledge base is incomplete, ambiguous, or insufficient - Ask the user for clarification. Do not make informed guesses.
        5. **Iterative Process:**
            - Continue searching your knowledge base till you have a comprehensive answer.
            - Reevaluate the completeness of your answer after each search iteration.
            - Repeat the search process until you are confident that every aspect of the question is addressed.
        4. **Reasoning Documentation:** Clearly document your reasoning process:
            - Note when additional searches were triggered.
            - Indicate which pieces of information came from the knowledge base and where it was sourced from.
            - Explain how you reconciled any conflicting or ambiguous information.
        5. **Final Synthesis:** Only finalize and present your answer once you have verified it through multiple search passes.
            Include all pertinent details and provide proper references.
        6. **Continuous Improvement:** If new, relevant information emerges even after presenting your answer,
            be prepared to update or expand upon your response.

        **Communication Style:**
        - Use clear and concise language.
        - Organize your response with numbered steps, bullet points, or short paragraphs as needed.
        - Be transparent about your search process and cite your sources.
        - Ensure that your final answer is comprehensive and leaves no part of the query unaddressed.

        Remember: **Do not finalize your answer until every angle of the question has been explored.**"""),
        additional_context=dedent("""\
        You should only respond with the final answer and the reasoning process.
        No need to include irrelevant information.

        - User ID: {user_id}
        - Memory: You have access to your previous search results and reasoning process.
        """),
        knowledge=agent_knowledge,
        db=agent_db,
        add_history_to_context=True,
        num_history_runs=3,
        read_chat_history=True,
        markdown=True,
        debug_mode=True,
    )

def get_agent_response(
    message: str, session_id: str, file_path: Optional[str] = None, model_id: Optional[str] = None
) -> str:
    """Run agent and return response as string (for UI integration)."""
    if not file_path:
        return "Please upload a file to begin."
    agent = create_agent(session_id=session_id, file_path=file_path, model_id=model_id)
    run_output = agent.run(message)
    response = run_output.content
    return response if isinstance(response, str) else str(response)
