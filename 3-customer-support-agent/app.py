import streamlit as st
from typing import TypedDict
from langgraph.graph import StateGraph, END
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
import os

st.set_page_config(page_title="Customer Support Agent", page_icon="🤖")
st.title("🤖 Customer Support Agent")

st.sidebar.title("Configuration")
api_key = st.sidebar.text_input("Enter your OpenAI API Key", type="password")

if api_key:
    os.environ["OPENAI_API_KEY"] = api_key

    class State(TypedDict):
        query: str
        category: str
        sentiment: str
        response: str

    def categorize(state: State) -> State:
        """Categorize the customer query into Technical, Billing, or General."""
        prompt = ChatPromptTemplate.from_template(
            "Categorize the following customer query into one of these categories: "
            "Technical, Billing, General. Query: {query}"
        )
        llm = ChatOpenAI(temperature=0)
        chain = prompt | llm
        category = chain.invoke({"query": state["query"]}).content
        return {"category": category}

    def analyze_sentiment(state: State) -> State:
        """Analyze the sentiment of the customer query as Positive, Neutral, or Negative."""
        prompt = ChatPromptTemplate.from_template(
            "Analyze the sentiment of the following customer query. "
            "Respond with either 'Positive', 'Neutral', or 'Negative'. Query: {query}"
        )
        llm = ChatOpenAI(temperature=0)
        chain = prompt | llm
        sentiment = chain.invoke({"query": state["query"]}).content
        return {"sentiment": sentiment}

    def handle_technical(state: State) -> State:
        """Provide a technical support response to the query."""
        prompt = ChatPromptTemplate.from_template(
            "Provide a technical support response to the following query: {query}"
        )
        llm = ChatOpenAI(temperature=0)
        chain = prompt | llm
        response = chain.invoke({"query": state["query"]}).content
        return {"response": response}

    def handle_billing(state: State) -> State:
        """Provide a billing support response to the query."""
        prompt = ChatPromptTemplate.from_template(
            "Provide a billing support response to the following query: {query}"
        )
        llm = ChatOpenAI(temperature=0)
        chain = prompt | llm
        response = chain.invoke({"query": state["query"]}).content
        return {"response": response}

    def handle_general(state: State) -> State:
        """Provide a general support response to the query."""
        prompt = ChatPromptTemplate.from_template(
            "Provide a general support response to the following query: {query}"
        )
        llm = ChatOpenAI(temperature=0)
        chain = prompt | llm
        response = chain.invoke({"query": state["query"]}).content
        return {"response": response}

    def escalate(state: State) -> State:
        """Escalate the query to a human agent due to negative sentiment."""
        return {"response": "This query has been escalated to a human agent due to its negative sentiment."}

    def route_query(state: State) -> str:
        """Route the query based on its sentiment and category."""
        if state["sentiment"] == "Negative":
            return "escalate"
        elif state["category"] == "Technical":
            return "handle_technical"
        elif state["category"] == "Billing":
            return "handle_billing"
        else:
            return "handle_general"

    # Create the graph
    workflow = StateGraph(State)

    # Add nodes
    workflow.add_node("categorize", categorize)
    workflow.add_node("analyze_sentiment", analyze_sentiment)
    workflow.add_node("handle_technical", handle_technical)
    workflow.add_node("handle_billing", handle_billing)
    workflow.add_node("handle_general", handle_general)
    workflow.add_node("escalate", escalate)

    # Add edges
    workflow.add_edge("categorize", "analyze_sentiment")
    workflow.add_conditional_edges(
        "analyze_sentiment",
        route_query,
        {
            "handle_technical": "handle_technical",
            "handle_billing": "handle_billing",
            "handle_general": "handle_general",
            "escalate": "escalate"
        }
    )
    workflow.add_edge("handle_technical", END)
    workflow.add_edge("handle_billing", END)
    workflow.add_edge("handle_general", END)
    workflow.add_edge("escalate", END)

    # Set entry point
    workflow.set_entry_point("categorize")

    # Compile the graph
    app = workflow.compile()

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                results = app.invoke({"query": prompt})
                response = results.get("response", "Sorry, I encountered an error.")
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
