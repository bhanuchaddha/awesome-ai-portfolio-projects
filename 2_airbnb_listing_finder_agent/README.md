# Agent: Airbnb Listing Finder Agent 🏠

---

**Public Access**  
https://airbnb-listing-finder-agent.streamlit.app/

**What This Agent Does**  
An AI agent that finds Airbnb listings based on your travel needs.
- Understands natural language queries.
- Searches, analyzes, and filters listings.
- Presents top 10 recommendations with direct links.

**Screenshots / Demo**  
See an example of the agent's output in [SAMPLE_RUN.md](./SAMPLE_RUN.md).

**Live Demo or API Endpoint**  
A local Streamlit UI is available.  
To run: `uv run streamlit run streamlit_app.py`

**Enterprise Business Impact**  
- *Before*: Manually searching for Airbnb listings is time-consuming and overwhelming.
- *After*: Automates search, delivering a curated list of the top 10 listings in minutes.
- *Why Build*: To streamline accommodation search and save user time.
- *Impact Metrics*: 
    - Reduces search time by up to 90%.
    - Improves match quality by applying all user-defined criteria.

**Who Should Use It**  
- **Travelers**: For efficient and personalized trip planning.
- **Travel Agencies**: To quickly source accommodation options for clients.
- **Real Estate Analysts**: For gathering data on short-term rental markets.

**Similar Agents / Code Reuse**  
The agent's logic is adaptable for other recommendation tasks:
- Restaurant finders
- Job search tools
- Product recommenders

**Technical Stack**  
- Python 3.12+
- Agno Framework
- OpenRouter (LLM provider)
- Model Context Protocol (MCP)
- Airbnb MCP Server

**How to Run Locally**  
1. Clone the repository.
2. `cd 2-airbnb-listing-finder-agent`
3. `uv sync`
4. Create `.env` with `OPENROUTER_API_KEY`.
5. CLI: `uv run 2-airbnb-listing-finder-agent.py`
6. Web UI: `uv run streamlit run streamlit_app.py`

**Contact / Maintainer**  
https://www.linkedin.com/in/bhanu-chaddha/

**License**  
MIT
