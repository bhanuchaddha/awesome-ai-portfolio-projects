# Competitor Analysis Agent 🔍

An intelligent AI agent that conducts comprehensive competitive landscape analysis by researching competitors, scraping their websites, and generating detailed strategic reports. Powered by advanced reasoning capabilities and web scraping tools, this agent helps businesses understand their competitive position and identify strategic opportunities.

## 📊 Introduction

Understanding your competitive landscape is crucial for strategic decision-making, but conducting thorough competitor analysis is time-consuming and requires extensive research across multiple sources. The Competitor Analysis Agent automates this process by leveraging AI-powered research, web scraping, and structured reasoning to deliver comprehensive competitive intelligence reports.

This project demonstrates how to build an intelligent research agent using AI frameworks, web scraping tools (Firecrawl via MCP), and reasoning capabilities. It showcases practical applications of AI in business intelligence and strategic analysis, making it an excellent addition to your AI portfolio.

## ✨ Features

- **Automated Competitor Discovery**: Identifies key competitors through intelligent web search
- **Website Scraping & Analysis**: Extracts detailed information from competitor websites using Firecrawl
- **Structured Reasoning**: Uses reasoning tools to plan research, analyze findings, and synthesize insights
- **Comprehensive Reports**: Generates detailed competitive analysis reports with:
  - Executive summaries
  - Market overview and industry context
  - Individual competitor profiles
  - SWOT analysis for each competitor
  - Feature and pricing comparisons
  - Strategic recommendations (short-term and long-term)
- **Multi-Source Research**: Aggregates information from industry reports, market analysis, and competitor websites
- **Strategic Insights**: Identifies competitive advantages, risks, and market opportunities
- **Evidence-Based Analysis**: Provides recommendations backed by gathered evidence

## 🛠️ Technologies Used

- **Python 3.12+**: Core programming language
- **Agno Framework**: AI agent framework for building intelligent assistants
- **OpenRouter**: LLM provider integration for natural language understanding and reasoning
- **MCP Tools (Firecrawl)**: Web scraping and content extraction via Model Context Protocol
- **ReasoningTools**: Structured thinking and analysis capabilities
- **Python-dotenv**: Environment variable management

## 📋 Prerequisites

Before you begin, ensure you have:

- Python 3.12 or higher installed
- `uv` package manager installed ([installation guide](https://github.com/astral-sh/uv))
- `npx` (Node.js package runner) - comes with Node.js ([install Node.js](https://nodejs.org/))
- An OpenRouter API key ([get one here](https://openrouter.ai/))

## 🚀 Setup Instructions

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd awesome-ai-portfolio-projects/5_competitor_analysis_agent
```

### 2. Install Dependencies

This project uses `uv` for dependency management. Install dependencies with:

```bash
uv sync
```

### 3. Configure Environment Variables

Create a `.env` file in the project directory:

```bash
touch .env
```

Add your API credentials:

```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
OPENROUTER_MODEL_ID=anthropic/claude-3.5-sonnet  # or your preferred model
```

### 4. Verify Installation

Check that all dependencies are installed correctly:

```bash
uv run python --version
```

Verify that `npx` is available (required for Firecrawl MCP):

```bash
npx --version
```

## 💻 Usage

### Basic Usage

Run the agent with the default example query (analyzes Maersk's competitors):

```bash
uv run 5_competitor_analysis_agent.py
```

### Custom Analysis

To analyze a different company, modify the `task` variable in `5_competitor_analysis_agent.py`:

```python
if __name__ == "__main__":
    task = """Analyze the competitive landscape for [Your Company Name] in the [Industry].
    """
    asyncio.run(run_agent(task))
```

### Example Queries

The agent can handle various types of competitive analysis requests:

#### Industry-Specific Analysis
```
"Analyze the competitive landscape for A.P. Moller - Maersk in the shipping industry."
"Research competitors for Stripe in the payment processing industry."
"Analyze the competitive position of Shopify in the e-commerce platform market."
```

#### Product-Focused Analysis
```
"Analyze competitors for Tesla in the electric vehicle market."
"Research the competitive landscape for OpenAI in the AI model provider space."
```

#### Market Segment Analysis
```
"Analyze competitors for Zoom in the video conferencing software market."
"Research the competitive landscape for Notion in the productivity software space."
```

## 🏗️ How It Works

### Architecture Overview

```
User Query
    ↓
Competitor Analysis Agent (Agno Framework)
    ↓
Reasoning Phase → Plan research approach
    ↓
Search Phase → Identify competitors via Firecrawl search
    ↓
Scraping Phase → Extract data from competitor websites
    ↓
Analysis Phase → Process findings with reasoning tools
    ↓
Synthesis Phase → Generate comprehensive report
    ↓
Structured Output → Present competitive analysis report
```

### Key Components

1. **Agent Configuration** (`5_competitor_analysis_agent.py`):
   - Sets up the Agno agent with OpenRouter model
   - Configures MCPTools with Firecrawl for web scraping
   - Integrates ReasoningTools for structured thinking
   - Defines comprehensive instructions for competitive analysis workflow

2. **Research Workflow**:
   The agent follows a structured 5-phase approach:
   
   - **Initial Research & Discovery**: Uses search tools to find information about the target company and identify competitors
   - **Competitor Identification**: Maps out the competitive landscape and identifies key players
   - **Website Analysis**: Scrapes competitor websites to extract product information, pricing, and value propositions
   - **Deep Competitive Analysis**: Compares features, pricing, and market positioning using reasoning tools
   - **Strategic Synthesis**: Conducts SWOT analysis and develops strategic recommendations

3. **MCP Tools Integration**:
   - Uses Firecrawl MCP server via `npx -y firecrawl-mcp`
   - Provides web scraping capabilities without direct API dependencies
   - Enables content extraction from competitor websites
   - Supports search functionality for discovering competitors

4. **Reasoning Tools**:
   - Enables structured thinking before major research phases
   - Helps analyze findings and draw insights
   - Supports multi-step reasoning for complex analysis
   - Provides confidence scores for research decisions

5. **Agent Instructions**:
   - Guides systematic research approach
   - Ensures thorough verification from multiple sources
   - Mandates evidence-based recommendations
   - Requires comprehensive report structure

### Analysis Process

1. **Planning**: Uses reasoning tools to plan research approach
2. **Discovery**: Searches for competitors and industry information
3. **Collection**: Scrapes competitor websites and gathers data
4. **Analysis**: Processes findings using reasoning tools
5. **Synthesis**: Generates structured competitive analysis report
6. **Recommendations**: Provides strategic insights and action items

## 📁 Project Structure

```
5_competitor_analysis_agent/
├── 5_competitor_analysis_agent.py  # Main agent script
├── pyproject.toml                   # Project dependencies and metadata
├── uv.lock                          # Locked dependency versions
├── SAMPLE_RUN.md                    # Example output from the agent
├── README.md                         # This file
└── .env                             # Environment variables (create this)
```

## 🔧 Configuration

### Model Selection

You can change the OpenRouter model in your `.env` file:

```env
OPENROUTER_MODEL_ID=anthropic/claude-3.5-sonnet
# Other options:
# OPENROUTER_MODEL_ID=openai/gpt-4-turbo
# OPENROUTER_MODEL_ID=google/gemini-pro
# OPENROUTER_MODEL_ID=meta-llama/llama-3.1-70b-instruct
```

### Agent Customization

Modify the agent's behavior by editing the `instructions` parameter:

- **Research Depth**: Adjust the number of competitors to analyze
- **Analysis Scope**: Modify focus areas (features, pricing, positioning, etc.)
- **Report Format**: Customize the expected output structure
- **Reasoning**: Enable/disable detailed reasoning steps

### MCP Tools Configuration

The agent uses Firecrawl via MCP (Model Context Protocol). The MCP server is automatically started using:

```python
mcp_tools = MCPTools(command="npx -y firecrawl-mcp")
```

You can customize this to use a different MCP server or configure Firecrawl settings.

## 📊 Report Structure

The agent generates comprehensive reports including:

### Executive Summary
- High-level overview of competitive landscape
- Key findings and insights

### Research Methodology
- Search queries used
- Websites analyzed
- Information sources

### Market Overview
- Industry context and trends
- Market size and growth
- Competitive landscape mapping

### Competitor Analysis
For each competitor:
- Company overview (website, founded, headquarters, size)
- Products & services
- Digital presence analysis
- SWOT analysis (Strengths, Weaknesses, Opportunities, Threats)

### Comparative Analysis
- Feature comparison matrix
- Pricing comparison
- Market positioning analysis

### Strategic Insights
- Key findings
- Competitive advantages
- Competitive risks

### Strategic Recommendations
- Immediate actions (0-3 months)
- Short-term strategy (3-12 months)
- Long-term strategy (12+ months)

## 🎯 Use Cases

This agent is perfect for:

- **Strategic Planning**: Understand competitive position before making strategic decisions
- **Market Research**: Conduct competitive intelligence for market entry or expansion
- **Product Development**: Identify gaps and opportunities in the competitive landscape
- **Sales Enablement**: Prepare competitive battle cards and positioning strategies
- **Investment Analysis**: Evaluate competitive dynamics for investment decisions
- **Startup Research**: Analyze competitors when launching a new product or service
- **Portfolio Demonstration**: Showcase AI agent development and business intelligence skills

## 🔍 Example Output

The agent provides structured output including:

- **Reasoning Steps**: Shows the agent's thinking process throughout the analysis
- **Tool Calls**: Displays search queries and scraping operations
- **Competitive Report**: Comprehensive markdown-formatted analysis
- **Strategic Recommendations**: Actionable insights organized by timeframe

See `SAMPLE_RUN.md` for a complete example output analyzing A.P. Moller - Maersk's competitive landscape in the shipping industry.

## 🚧 Limitations & Considerations

- **API Rate Limits**: Be mindful of OpenRouter and Firecrawl API rate limits
- **Data Accuracy**: Information depends on web search results and may need verification
- **Website Access**: Some competitor websites may block scraping or require authentication
- **Market Coverage**: Analysis quality depends on available information online
- **Real-Time Data**: Doesn't provide real-time financial or market data
- **Subjective Analysis**: Insights are based on AI interpretation of available information

## 🔮 Future Enhancements

Potential improvements for this project:

- **Financial Data Integration**: Incorporate financial APIs for revenue, market share, and growth metrics
- **News & Social Media**: Analyze competitor mentions in news and social media
- **Patent Analysis**: Research competitor patents and intellectual property
- **Review Analysis**: Analyze customer reviews and sentiment for competitors
- **Historical Trends**: Track competitive changes over time
- **Export Formats**: Support PDF, Excel, and other export formats
- **Visualizations**: Generate charts and graphs for competitive comparisons
- **Custom Report Templates**: Allow users to customize report structure
- **Multi-Language Support**: Analyze competitors in different languages
- **Alert System**: Monitor competitors and alert on significant changes

## 📚 Learning Outcomes

By working with this project, you'll learn:

- How to build AI agents using the Agno framework
- Integrating MCP (Model Context Protocol) tools with AI assistants
- Using reasoning tools for structured analysis
- Web scraping and content extraction strategies
- Building comprehensive research workflows
- Structuring agent instructions for complex tasks
- Creating business intelligence applications
- Designing strategic analysis systems

## 💡 Key Features Demonstrated

This project showcases several important AI and software engineering concepts:

1. **Agent Architecture**: Building research-focused AI agents with reasoning capabilities
2. **MCP Integration**: Using Model Context Protocol for tool integration
3. **Structured Reasoning**: Implementing multi-step reasoning workflows
4. **Web Scraping**: Extracting and processing information from websites
5. **Business Intelligence**: Creating actionable insights from raw data
6. **Report Generation**: Structuring complex information into readable formats
7. **Strategic Analysis**: Applying analytical frameworks (SWOT, competitive analysis)

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

- Enhanced scraping strategies and error handling
- Additional data sources (financial APIs, news APIs)
- Better competitor identification algorithms
- Improved report formatting and visualization
- Unit tests and integration tests
- Performance optimizations
- Support for additional MCP tools

## 📄 License

This project is part of the Awesome AI Portfolio Projects collection and is licensed under the MIT License.

## 🔗 Related Projects

- [Bookey - The Book Recommender Agent](./../4-bookey_the_book_recommender_agent/) - Similar recommendation system using AI agents
- [Airbnb Listing Finder Agent](./../2-airbnb-listing-finder-agent/) - Similar search and analysis agent
- [MCP Server from Any API](./../1-mcp-server-from-any-api/) - Learn how to create MCP servers
- More projects coming soon!

## 🙏 Acknowledgments

- **Agno Framework**: For providing the agent infrastructure
- **Firecrawl**: For web scraping capabilities via MCP
- **OpenRouter**: For LLM access
- **MCP Protocol**: For standardized tool integration

---

⭐ **Star this repository** if you find this project helpful for your AI learning journey!

**Happy Analyzing! 🔍✨**

