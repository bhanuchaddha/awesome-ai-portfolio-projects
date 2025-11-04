# Airbnb Listing Finder Agent 🏠

An intelligent AI agent that helps you find the perfect Airbnb listings based on your travel requirements. This agent uses the Model Context Protocol (MCP) to connect with Airbnb's search capabilities and leverages reasoning tools to provide thoughtful, well-organized recommendations.

## 📖 Introduction

Finding the right Airbnb accommodation can be time-consuming and overwhelming, especially when you have specific requirements like location, amenities, dates, and budget constraints. The Airbnb Listing Finder Agent simplifies this process by acting as your intelligent travel assistant.

Using advanced AI reasoning capabilities, the agent:
- Understands your natural language travel requirements
- Searches Airbnb listings based on your criteria
- Analyzes and filters results to match your preferences
- Presents recommendations in an organized, easy-to-understand format
- Provides direct links to listings for easy booking

This project demonstrates how to build an AI agent that combines MCP tools with reasoning capabilities to solve real-world problems, making it an excellent addition to your AI portfolio.

## ✨ Features

- **Natural Language Processing**: Describe your travel needs in plain English
- **Intelligent Search**: Automatically searches Airbnb with optimal parameters
- **Reasoning Capabilities**: Uses step-by-step reasoning to refine searches and validate results
- **Smart Filtering**: Focuses on listings that match your specific requirements (bedrooms, amenities, location, etc.)
- **Organized Results**: Presents top 10 recommendations in well-formatted tables
- **Direct Links**: Provides clickable links to each listing for easy access
- **Date-Aware**: Handles check-in/check-out dates intelligently
- **Location Proximity**: Considers proximity to landmarks and points of interest

## 🛠️ Technologies Used

- **Python 3.12+**: Core programming language
- **Agno Framework**: AI agent framework for building intelligent assistants
- **OpenRouter**: LLM provider integration
- **Model Context Protocol (MCP)**: Protocol for connecting AI assistants to external tools
- **Airbnb MCP Server**: Pre-built MCP server for Airbnb search functionality
- **Reasoning Tools**: Step-by-step reasoning capabilities for complex problem-solving

## 📋 Prerequisites

Before you begin, ensure you have:

- Python 3.12 or higher installed
- `uv` package manager installed ([installation guide](https://github.com/astral-sh/uv))
- An OpenRouter API key ([get one here](https://openrouter.ai/))
- Node.js installed (for running the Airbnb MCP server)

## 🚀 Setup Instructions

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd awesome-ai-portfolio-projects/2-airbnb-listing-finder-agent
```

### 2. Install Dependencies

This project uses `uv` for dependency management. Install dependencies with:

```bash
uv sync
```

### 3. Configure Environment Variables

Create a `.env` file in the project directory:

```bash
cp .env.example .env  # If you have an example file
# Or create .env manually
```

Add your OpenRouter credentials:

```env
OPENROUTER_API_KEY=your_api_key_here
OPENROUTER_MODEL_ID=anthropic/claude-3.5-sonnet  # or your preferred model
```

### 4. Verify Installation

Check that all dependencies are installed correctly:

```bash
uv run python --version
```

## 💻 Usage

### Basic Usage

Run the agent with the default example query:

```bash
uv run 2-airbnb-listing-finder-agent.py
```

### Custom Queries

To use the agent with your own queries, modify the `task` variable in `2-airbnb-listing-finder-agent.py`:

```python
task = dedent("""
I'm traveling to Paris from March 15th - March 22nd. 
Can you find me a 2-bedroom apartment with a kitchen?
I'd like it to be close to the Eiffel Tower and under $200 per night.
""")
```

### Example Queries

Here are some example queries you can try:

**Budget-focused search:**
```
Find me affordable Airbnb listings in Tokyo for next week. 
I need a studio apartment with WiFi.
```

**Location-specific search:**
```
I'm visiting New York from Dec 20-27. 
Find me a 1-bedroom apartment in Manhattan near Central Park 
with a dedicated workspace.
```

**Amenity-focused search:**
```
Looking for a pet-friendly Airbnb in San Francisco 
for the first week of February. 
Need parking and a washing machine.
```

## 🏗️ How It Works

### Architecture Overview

```
User Query
    ↓
Agent (Agno Framework)
    ↓
Reasoning Tools → Analyze requirements & plan search strategy
    ↓
MCP Tools → Connect to Airbnb MCP Server
    ↓
Airbnb Search API → Execute search with optimized parameters
    ↓
Results Analysis → Filter and rank listings
    ↓
Formatted Output → Present top 10 recommendations
```

### Key Components

1. **Agent Configuration** (`2-airbnb-listing-finder-agent.py`):
   - Sets up the Agno agent with OpenRouter model
   - Configures reasoning tools for step-by-step problem solving
   - Connects to Airbnb MCP server via MCPTools
   - Defines agent instructions for consistent behavior

2. **Reasoning Tools**:
   - Helps the agent break down complex queries
   - Validates search results before presenting them
   - Ensures all requirements are met

3. **Airbnb MCP Server**:
   - Provides `airbnb_search` tool for querying listings
   - Handles search parameters (location, dates, filters)
   - Returns structured listing data

4. **Agent Instructions**:
   - Guides the agent to use reasoning tools at each step
   - Ensures results are presented in organized tables
   - Requires direct links to listings
   - Focuses on providing top 10 recommendations with justifications

### Reasoning Process

The agent follows a structured reasoning approach:

1. **Understanding**: Parses user requirements (location, dates, preferences)
2. **Planning**: Determines optimal search parameters
3. **Execution**: Performs Airbnb search via MCP tools
4. **Validation**: Checks if results meet all requirements
5. **Refinement**: Adjusts search if needed (broader location, different dates, etc.)
6. **Presentation**: Formats and presents top recommendations

## 📁 Project Structure

```
2-airbnb-listing-finder-agent/
├── 2-airbnb-listing-finder-agent.py  # Main agent script
├── pyproject.toml                     # Project dependencies and metadata
├── uv.lock                           # Locked dependency versions
├── README.md                         # This file
└── .env                              # Environment variables (create this)
```

## 🔧 Configuration

### Model Selection

You can change the OpenRouter model in your `.env` file:

```env
OPENROUTER_MODEL_ID=anthropic/claude-3.5-sonnet
# Other options:
# OPENROUTER_MODEL_ID=openai/gpt-4-turbo
# OPENROUTER_MODEL_ID=google/gemini-pro
```

### Agent Instructions

Customize agent behavior by modifying the `instructions` parameter in the agent configuration. The current instructions:
- Enforce reasoning tool usage at each step
- Require table-formatted outputs
- Emphasize providing links and top 10 recommendations
- Include validation steps

## 🎯 Use Cases

This agent is perfect for:

- **Travel Planning**: Quickly find suitable accommodations for your trips
- **Budget Research**: Compare prices across different dates and locations
- **Location Scouting**: Find properties near specific landmarks or areas
- **Amenity Matching**: Search for listings with specific features
- **Portfolio Demonstration**: Showcase AI agent development skills

## 🔍 Example Output

The agent provides structured output including:

- **Top 10 Recommendations Table**: Listing ID, name, price, total cost, and direct links
- **Reasoning Steps**: Transparent explanation of the search process
- **Filtering Rationale**: Why certain listings were selected
- **Additional Tips**: Helpful suggestions for further refinement

## 🚧 Limitations & Considerations

- **Rate Limits**: Be mindful of API rate limits when making multiple searches
- **Data Accuracy**: Listing availability and prices change frequently on Airbnb
- **Robots.txt**: The agent can be configured to ignore robots.txt (default behavior)
- **Search Quality**: Results depend on Airbnb's search API capabilities

## 🔮 Future Enhancements

Potential improvements for this project:

- **Save Favorite Listings**: Persist preferred listings for later reference
- **Price Tracking**: Monitor price changes for specific listings
- **Comparison Tools**: Side-by-side comparison of multiple listings
- **Calendar Integration**: Check availability across multiple date ranges
- **Multi-City Planning**: Plan accommodations for multi-city trips
- **User Preferences**: Remember user preferences for personalized searches

## 📚 Learning Outcomes

By working with this project, you'll learn:

- How to build AI agents using the Agno framework
- Integrating MCP tools with AI assistants
- Using reasoning tools for complex problem-solving
- Natural language query processing
- Structuring agent instructions for consistent behavior
- Working with external APIs through MCP protocol

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

- Enhanced error handling
- Additional search filters
- Result caching mechanisms
- Better output formatting
- Unit tests and integration tests

## 📄 License

This project is part of the Awesome AI Portfolio Projects collection and is licensed under the MIT License.

## 🔗 Related Projects

- [MCP Server from Any API](./../1-mcp-server-from-any-api/) - Learn how to create MCP servers
- More projects coming soon!

---

⭐ **Star this repository** if you find this project helpful for your AI learning journey!
