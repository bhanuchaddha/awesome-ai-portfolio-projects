# Agent: Competitor Analysis Agent 🔍

---

**Public Access**  
https://competitor-analysis-agent.streamlit.app/

**What This Agent Does**  
This agent automates competitive analysis by:
- Identifying key competitors through intelligent web searches.
- Scraping competitor websites to extract product details, pricing, and features.
- Generating comprehensive strategic reports, including SWOT analysis and market positioning.
- Providing actionable recommendations to help businesses gain a competitive edge.

**Screenshots / Demo**  
A sample output of a full analysis run by the agent is available in [`SAMPLE_RUN.md`](./SAMPLE_RUN.md).

You can also run the interactive demo using Streamlit.

**Live Demo or API Endpoint**  
https://competitor-analysis-agent.streamlit.app/
To run the live demo locally, execute the following command in your terminal:
```bash
streamlit run streamlit_app.py
```

**Enterprise Business Impact**  
- *Before*: Competitor analysis was a manual, time-consuming process that often took weeks and resulted in outdated insights.
- *After*: The agent delivers comprehensive, real-time competitive reports in minutes, enabling agile strategic decision-making.
- *Why Build*: To provide businesses with a powerful, automated tool for continuous competitive intelligence, reducing manual effort and cost.
- *Impact Metrics*: 
  - Reduces research time by over 95%.
  - Improves data accuracy for strategic planning.
  - Identifies market opportunities and threats faster.

**Who Should Use It**  
This agent is valuable for:
- **Strategic Planners**: For data-driven strategic decisions.
- **Market Researchers**: To automate competitive intelligence gathering.
- **Product Managers**: To identify feature gaps and opportunities.
- **Sales & Marketing Teams**: To create competitive battle cards.
- **Investment Analysts**: For evaluating market dynamics.
- **Startups**: To analyze the competitive landscape for new ventures.

**Similar Agents / Code Reuse**  
The underlying architecture can be adapted for other research-intensive tasks. Related projects include:
- [Bookey - The Book Recommender Agent](./../4-bookey_the_book_recommender_agent/)
- [Airbnb Listing Finder Agent](./../2_airbnb_listing_finder_agent/)

**Technical Stack**  
- **Core**: Python 3.12+
- **AI Framework**: Agno Framework
- **LLM Provider**: OpenRouter
- **Web Scraping**: MCP Tools (Firecrawl)
- **Reasoning**: ReasoningTools
- **UI Demo**: Streamlit

**How to Run Locally**  
1. **Clone the repository:**
   ```bash
   git clone https://github.com/bhanuchaddha/enterprise-ai-agents.git
   cd enterprise-ai-agents/5_competitor_analysis_agent
   ```
2. **Install dependencies:**
   ```bash
   uv sync
   ```
3. **Configure environment variables:**
   Create a `.env` file and add your `OPENROUTER_API_KEY`.
4. **Run the agent:**
   ```bash
   uv run 5_competitor_analysis_agent.py
   ```
5. **Run the interactive demo:**
   ```bash
   streamlit run streamlit_app.py
   ```

**Contact / Maintainer**  
[Bhanu Chaddha on LinkedIn](https://www.linkedin.com/in/bhanu-chaddha/)

**License**  
This project is licensed under the MIT License.

