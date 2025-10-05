# Customer Support Agent

This tutorial demonstrates how to create an intelligent customer support agent using Streamlit and LangGraph. The agent is designed to categorize customer queries, analyze sentiment, and provide appropriate responses or escalate issues when necessary.

## How it Works

The agent uses a graph-based workflow built with LangGraph to process customer queries. The workflow consists of the following steps:

1.  **Categorization:** The agent first categorizes the query into one of three categories: `Technical`, `Billing`, or `General`.
2.  **Sentiment Analysis:** Next, it analyzes the sentiment of the query to determine if it is `Positive`, `Neutral`, or `Negative`.
3.  **Routing:** Based on the sentiment and category, the agent routes the query to the appropriate handler:
    *   If the sentiment is `Negative`, the query is escalated to a human agent.
    *   If the sentiment is `Positive` or `Neutral`, the query is handled by a specialized function based on its category.

## How to Run

1.  **Install Dependencies:**

    ```bash
    uv pip install -r requirements.txt
    ```

2.  **Set API Keys:**

    The application requires an OpenAI API key. You can enter it in the sidebar of the application.

3.  **Run the Application:**

    ```bash
    streamlit run app.py
    ```

## How to Test

You can test the agent's functionality by entering different queries in the chat interface. Here are some examples:

### Technical Support

*   **Query:** "My internet connection keeps dropping. Can you help?"
*   **Expected Outcome:** This query has a negative sentiment and will be escalated.

*   **Query:** "I need help talking to chatGPT"
*   **Expected Outcome:** This query will be categorized as `Technical` and handled accordingly.

### Billing Support

*   **Query:** "Where can I find my receipt?"
*   **Expected Outcome:** This query will be categorized as `Billing` and handled accordingly.

### General Support

*   **Query:** "What are your business hours?"
*   **Expected Outcome:** This query will be categorized as `General` and handled accordingly.
