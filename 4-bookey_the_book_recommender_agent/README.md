# Bookey - The Book Recommender Agent 📚

An intelligent AI agent that provides comprehensive, personalized book recommendations based on your reading preferences, favorite books, and literary interests. Powered by advanced search capabilities and deep literary knowledge, Bookey helps you discover your next favorite read.

## 📖 Introduction

Finding your next great read can be overwhelming with millions of books available across countless genres. Bookey simplifies this process by acting as your personal literary curator. Whether you're looking for books similar to ones you've loved, exploring new genres, or seeking the latest releases, Bookey combines book databases, ratings, reviews, and upcoming releases to deliver thoughtful recommendations.

This project demonstrates how to build an intelligent recommendation system using AI agents, web search capabilities, and natural language processing. It showcases practical applications of AI in content discovery and personalization, making it an excellent addition to your AI portfolio.

## ✨ Features

- **Personalized Recommendations**: Get book suggestions based on your favorite reads and preferences
- **Comprehensive Book Information**: Access detailed data including ratings, genres, page counts, and plot summaries
- **Multi-Source Search**: Leverages Exa search to find books from various databases and review sites
- **Genre Exploration**: Discover books across fiction, non-fiction, fantasy, romance, and more
- **Rating Integration**: Includes Goodreads/StoryGraph ratings to help you choose quality reads
- **Content Advisories**: Provides trigger warnings and content notes when relevant
- **Series Information**: Identifies books that are part of series or have companion novels
- **Audiobook Availability**: Notes when audiobook versions are available
- **Adaptation Tracking**: Mentions upcoming TV/film adaptations
- **Diverse Recommendations**: Ensures variety in authors and perspectives
- **Natural Language Queries**: Ask for recommendations in plain English

## 🛠️ Technologies Used

- **Python 3.12+**: Core programming language
- **Agno Framework**: AI agent framework for building intelligent assistants
- **OpenRouter**: LLM provider integration for natural language understanding
- **Exa Tools**: Advanced search capabilities for finding book information
- **Python-dotenv**: Environment variable management

## 📋 Prerequisites

Before you begin, ensure you have:

- Python 3.12 or higher installed
- `uv` package manager installed ([installation guide](https://github.com/astral-sh/uv))
- An OpenRouter API key ([get one here](https://openrouter.ai/))
- An Exa API key ([get one here](https://exa.ai/))

## 🚀 Setup Instructions

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd awesome-ai-portfolio-projects/4-bookey_the_book_recommender_agent
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
EXA_API_KEY=your_exa_api_key_here
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
uv run 4-bookey_the_book_recommender_agent.py
```

### Custom Queries

To use the agent with your own queries, modify the `print_response` call in `4-bookey_the_book_recommender_agent.py`:

```python
book_recommendation_agent.print_response(
    "I love science fiction books with strong female protagonists. What do you recommend?",
    stream=True,
)
```

### Example Queries

The agent can handle various types of book recommendation requests:

#### Based on Favorite Books
```
"I really enjoyed 'Anxious People' and 'Lessons in Chemistry', can you suggest similar books?"
"I am reading 'Psychology of Money' by Morgan Housel, can you suggest similar books?"
"Recommend books similar to 'The Seven Husbands of Evelyn Hugo'"
```

#### Genre-Specific Queries
```
"Recommend contemporary literary fiction like 'Beautiful World, Where Are You'"
"What are the best fantasy series completed in the last 5 years?"
"Find me atmospheric gothic novels like 'Mexican Gothic' and 'Ninth House'"
"What are the most acclaimed debut novels from this year?"
```

#### Thematic Queries
```
"Suggest books about climate change that aren't too depressing"
"What are the best books about artificial intelligence for non-technical readers?"
"Recommend memoirs about immigrant experiences"
"Find me books about mental health with hopeful endings"
```

#### Book Club & Practical Queries
```
"What are good book club picks that spark discussion?"
"Suggest literary fiction under 350 pages"
"Find thought-provoking novels that tackle current social issues"
"Recommend books with multiple perspectives/narratives"
```

#### Upcoming Releases
```
"What are the most anticipated literary releases next month?"
"Show me upcoming releases from my favorite authors"
"What debut novels are getting buzz this season?"
"List upcoming books being adapted for screen"
```

## 🏗️ How It Works

### Architecture Overview

```
User Query
    ↓
Bookey Agent (Agno Framework)
    ↓
Analysis Phase → Understand preferences & identify themes
    ↓
Exa Search Tools → Search for relevant books
    ↓
Curate Results → Filter and organize recommendations
    ↓
Detailed Information → Gather ratings, summaries, metadata
    ↓
Formatted Output → Present structured recommendations
```

### Key Components

1. **Agent Configuration** (`4-bookey_the_book_recommender_agent.py`):
   - Sets up the Agno agent with OpenRouter model
   - Configures ExaTools for book search capabilities
   - Defines agent personality as "Bookey" - a passionate literary curator
   - Includes detailed instructions for recommendation workflow

2. **Recommendation Workflow**:
   The agent follows a structured 4-phase approach:
   
   - **Analysis Phase**: Understands reader preferences, analyzes mentioned books' themes and styles, factors in specific requirements
   - **Search & Curate**: Uses Exa to search for relevant books, ensures diversity, verifies current and accurate data
   - **Detailed Information**: Provides comprehensive book details including title, author, publication year, genre, ratings, page count, plot summary, content advisories, and awards
   - **Extra Features**: Includes series information, similar author suggestions, audiobook availability, and adaptation notes

3. **Exa Search Integration**:
   - Searches across multiple book databases and review sites
   - Retrieves current information about books, ratings, and reviews
   - Enables discovery of both popular and niche recommendations

4. **Agent Instructions**:
   - Guides the agent to provide minimum 5 recommendations per query
   - Requires structured markdown formatting with tables
   - Emphasizes diversity in authors and perspectives
   - Includes emoji indicators for visual organization
   - Mandates content warnings when relevant

### Recommendation Process

1. **Understanding**: Parses user query to identify preferences, favorite books, genres, and requirements
2. **Theme Analysis**: Extracts themes, styles, and elements from mentioned books
3. **Search Execution**: Uses Exa to find books matching identified criteria
4. **Curation**: Filters and organizes results ensuring diversity and quality
5. **Enrichment**: Gathers additional information (ratings, summaries, metadata)
6. **Presentation**: Formats recommendations in structured tables with detailed explanations

## 📁 Project Structure

```
4-bookey_the_book_recommender_agent/
├── 4-bookey_the_book_recommender_agent.py  # Main agent script
├── pyproject.toml                           # Project dependencies and metadata
├── uv.lock                                 # Locked dependency versions
├── SAMPLE_RUN.md                           # Example output from the agent
├── README.md                               # This file
└── .env                                    # Environment variables (create this)
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

Modify the agent's personality and behavior by editing the `description` and `instructions` parameters:

- **Description**: Defines the agent's personality and expertise
- **Instructions**: Controls the recommendation workflow and output format
- **Markdown**: Enabled for formatted output
- **Datetime Context**: Adds current date/time for time-sensitive queries

### Search Parameters

Adjust Exa search behavior through the agent instructions:
- Number of results to retrieve
- Search categories and filters
- Result diversity requirements

## 🎯 Use Cases

This agent is perfect for:

- **Personal Reading Discovery**: Find your next favorite book based on what you've enjoyed
- **Book Club Planning**: Discover discussion-worthy books that match your group's interests
- **Genre Exploration**: Venture into new genres with curated recommendations
- **Gift Giving**: Find the perfect book for friends and family
- **Academic Research**: Discover relevant books for research topics
- **Portfolio Demonstration**: Showcase AI agent development and recommendation system skills

## 🔍 Example Output

The agent provides structured output including:

- **Recommendations Table**: Book title, author, publication year, genre, and ratings
- **Detailed Information**: Page count, plot summaries, content advisories, and awards
- **Extra Features**: Series information, audiobook availability, and adaptation notes
- **Explanation**: Why each book was recommended and how it matches your preferences
- **Diversity Notes**: Ensures variety in authors and perspectives

See `SAMPLE_RUN.md` for complete example outputs.

## 🚧 Limitations & Considerations

- **API Rate Limits**: Be mindful of Exa and OpenRouter API rate limits
- **Data Accuracy**: Book information depends on web search results and may need verification
- **Subjectivity**: Recommendations are based on AI interpretation of your preferences
- **Availability**: Doesn't check actual book availability at retailers or libraries
- **Coverage**: May have limited information about very new or obscure books

## 🔮 Future Enhancements

Potential improvements for this project:

- **Reading List Management**: Save and manage personalized reading lists
- **Progress Tracking**: Track reading progress and provide recommendations based on current reads
- **Social Features**: Share recommendations and see what friends are reading
- **Price Comparison**: Compare prices across different retailers
- **Library Integration**: Check availability at local libraries
- **Review Aggregation**: Aggregate reviews from multiple sources
- **Reading Goals**: Set and track annual reading goals
- **Genre Analytics**: Visualize reading preferences and patterns

## 📚 Learning Outcomes

By working with this project, you'll learn:

- How to build AI agents using the Agno framework
- Integrating search tools (Exa) with AI assistants
- Creating personalized recommendation systems
- Natural language query processing for content discovery
- Structuring agent instructions for consistent behavior
- Working with book databases and metadata
- Designing user-friendly recommendation interfaces

## 💡 Key Features Demonstrated

This project showcases several important AI and software engineering concepts:

1. **Agent Architecture**: Building conversational AI agents with personality
2. **Tool Integration**: Connecting external APIs (Exa) to AI agents
3. **Recommendation Algorithms**: Creating personalized content recommendations
4. **Natural Language Understanding**: Processing user queries in plain English
5. **Data Curation**: Filtering and organizing search results
6. **Structured Output**: Formatting recommendations in readable formats

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

- Enhanced search strategies
- Additional data sources (Goodreads API, Google Books API)
- Better error handling and edge cases
- Unit tests and integration tests
- Performance optimizations
- UI/UX improvements for recommendations

## 📄 License

This project is part of the Awesome AI Portfolio Projects collection and is licensed under the MIT License.

## 🔗 Related Projects

- [Airbnb Listing Finder Agent](./../2-airbnb-listing-finder-agent/) - Similar recommendation system for accommodations
- [MCP Server from Any API](./../1-mcp-server-from-any-api/) - Learn how to create MCP servers
- More projects coming soon!

## 🙏 Acknowledgments

- **Agno Framework**: For providing the agent infrastructure
- **Exa**: For powerful search capabilities
- **OpenRouter**: For LLM access
- The book-loving community for inspiration

---

⭐ **Star this repository** if you find this project helpful for your AI learning journey!

**Happy Reading! 📖✨**

