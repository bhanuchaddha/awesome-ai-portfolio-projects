# Agent: Deep Knowledge Agent 📚

---

**What This Agent Does**  
This agent performs iterative searches through its knowledge base, breaking down complex queries into sub-questions, and synthesizing comprehensive answers. It’s designed to explore topics deeply and thoroughly by following chains of reasoning. In this example, the agent uses the Agno documentation as a knowledge base.

**Key Features**:
* Iteratively searches a knowledge base
* Breaks down complex topics
* Source attribution and citations

**Demo**  
You can run the interactive demo using Streamlit.

To run the live demo locally, execute the following command in your terminal:
```bash
streamlit run 1_deep_knowledge_agent/streamlit_app.py
```

**Enterprise Business Impact**  
- *Before*: Obtaining deep, well-researched answers on complex topics required significant manual research, often leading to incomplete or inconsistent information.
- *After*: The agent provides in-depth, synthesized answers from a knowledge base, complete with citations, in a fraction of the time.
- *Why Build*: To empower users with a reliable tool for deep research, reducing the time spent on information gathering and improving the quality of insights.
- *Impact Metrics*: 
  - Drastically reduces time spent on research tasks.
  - Improves the accuracy and depth of information for decision-making.
  - Ensures consistency in answers by using a centralized knowledge base.

**Who Should Use It**  
This agent is valuable for:
- **Researchers**: To quickly get up to speed on new topics.
- **Analysts**: For detailed information gathering and synthesis.
- **Content Creators**: To research topics for articles, reports, or presentations.
- **Students & Academics**: For study and literature review.

**Technical Stack**  
- **Core**: Python 3.9+
- **AI Framework**: Agno Framework
- **LLM Provider**: OpenAI
- **Vector DB**: LanceDB
- **Knowledge Embedding**: OpenAI Embedder
- **UI Demo**: Streamlit

**How to Run Locally**  
1. **Navigate to the agent directory:**
   ```bash
   cd 1_deep_knowledge_agent
   ```
2. **Create a virtual environment and install dependencies:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt 
   ```
   *Note: For the first run, you might need to create the `pyproject.toml` from the dependencies listed in the file.*
   I will be using `uv` to manage dependencies.
   ```bash
   uv sync
   ```
3. **Configure environment variables:**
   Create a `.env` file in this directory and add your `OPENAI_API_KEY`.
   ```
   OPENAI_API_KEY="your-openai-api-key"
   ```
4. **Run the interactive demo:**
   ```bash
   streamlit run streamlit_app.py
   ```

**Contact / Maintainer**  
[Bhanu Chaddha on LinkedIn](https://www.linkedin.com/in/bhanu-chaddha/)

**License**  
This project is licensed under the MIT License.
