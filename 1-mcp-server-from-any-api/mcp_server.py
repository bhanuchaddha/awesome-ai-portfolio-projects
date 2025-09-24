"""
MCP Server for FastAPI Todo Application using FastMCP

This module mounts an MCP server back into the original FastAPI app,
providing both regular API endpoints and LLM-friendly MCP endpoints.
"""

from fastmcp import FastMCP
from fastapi import FastAPI, APIRouter
import uvicorn
from app.main import api_app

# 1. Create an app that includes the API routes at /api for MCP generation
mcp_source_app = FastAPI(title="Todo API for MCP")

# Create a router with /api prefix and include all the todo routes
api_router = APIRouter(prefix="/api")
api_router.include_router(api_app.router)
mcp_source_app.include_router(api_router)

# 2. Generate MCP server from the properly prefixed API
mcp = FastMCP.from_fastapi(app=mcp_source_app, name="Todo MCP")

# 3. Create the MCP's ASGI app
mcp_app = mcp.http_app(path='/mcp')

# 4. Create the main combined app
app = FastAPI(title="Todo API with MCP", lifespan=mcp_app.lifespan)

# Mount the original API at /api
app.mount("/api", api_app)

# Mount the MCP server at /llm
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