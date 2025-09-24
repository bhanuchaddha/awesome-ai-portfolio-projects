"""
MCP Server for FastAPI Todo Application using FastMCP

This module mounts an MCP server back into the original FastAPI app,
providing both regular API endpoints and LLM-friendly MCP endpoints.
"""

from fastmcp import FastMCP
from fastapi import FastAPI
import uvicorn
from app.main import api_app as todo_api

# 1. Generate MCP server from your API
mcp = FastMCP.from_fastapi(app=todo_api, name="Todo MCP")

# 2. Create the MCP's ASGI app
mcp_app = mcp.http_app(path='/mcp')

# 3. Create a new FastAPI app and mount everything
app = FastAPI(title="Todo API with MCP", lifespan=mcp_app.lifespan)

# Mount the original API routes
app.mount("/api", todo_api)

# Mount the MCP server
app.mount("/llm", mcp_app)

# Root endpoint for the combined app
@app.get("/")
async def root():
    return {
        "message": "Todo API with MCP support",
        "endpoints": {
            "api": "http://localhost:8000/api/todos",
            "api_docs": "http://localhost:8000/api/docs", 
            "mcp": "http://localhost:8000/llm/mcp/",
            "mcp_docs": "http://localhost:8000/llm/docs"
        }
    }

if __name__ == "__main__":
    print("Starting combined FastAPI + MCP server...")
    print("API endpoints: http://localhost:8000/api/")
    print("MCP endpoints: http://localhost:8000/llm/mcp/")
    print("API docs: http://localhost:8000/api/docs")
    print("MCP docs: http://localhost:8000/llm/docs")
    
    uvicorn.run("mcp_server:app", host="0.0.0.0", port=8000, reload=True)