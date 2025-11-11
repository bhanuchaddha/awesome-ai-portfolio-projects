# Blog Post Generator Agent ✍️

A powerful multi-agent content creation pipeline that transforms a topic into a complete content suite: research, blog post, LinkedIn post, and Twitter thread.

## Architecture

The system uses **4 specialized agents** working in sequence:

### 1. 🔍 Research Agent
- Uses Exa to search for 5-7 high-quality, authoritative sources
- Extracts key facts, statistics, and expert insights
- Organizes findings into a structured research summary
- **Output**: Comprehensive research with citations

### 2. ✍️ Blog Writer Agent
- Transforms research data into engaging blog posts
- Creates SEO-optimized content with proper structure
- Includes headlines, sections, takeaways, and citations
- **Output**: Publication-ready blog post

### 3. 💼 LinkedIn Agent
- Converts blog content into professional LinkedIn posts
- Optimizes for LinkedIn's audience and algorithm
- Adds engagement hooks and hashtag suggestions
- **Output**: LinkedIn post (3-4 paragraphs + hashtags)

### 4. 🐦 Twitter Agent
- Creates viral-worthy Twitter threads from blog content
- Respects 280-character limit per tweet
- Adds hooks, insights, and calls-to-action
- **Output**: Twitter thread (3-5 tweets)

## Pipeline Flow

```
Topic Input
    ↓
🔍 Research Agent (Exa Search)
    ↓
✍️ Blog Writer Agent
    ↓
    ├── 💼 LinkedIn Agent
    └── 🐦 Twitter Agent (parallel)
    ↓
Complete Content Suite
```

## How to run

1.  **Install dependencies**:
    ```bash
    uv pip install -r requirements.txt
    ```
    (Note: `pyproject.toml` is used, `uv` will handle it).

2.  **Set up your environment variables**:
    Create a `.env` file in the root of the project and add your API keys:
    ```
    OPENROUTER_API_KEY="your-openrouter-api-key"
    OPENROUTER_MODEL_ID="minimax/minimax-m2:free"  # Optional, defaults to minimax/minimax-m2:free
    EXA_API_KEY="your-exa-api-key"
    ```

3.  **Run the Streamlit app**:
    ```bash
    streamlit run 6_blog_post_generator_agent/streamlit_app.py
    ```
