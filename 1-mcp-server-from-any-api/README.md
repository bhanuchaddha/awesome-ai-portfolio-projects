# Converting FastAPI to MCP Server Tutorial

This tutorial demonstrates how to convert any FastAPI application into a Model Context Protocol (MCP) server. You'll build a simple Todo API and expose it as MCP tools that can be used by AI assistants.

## What You'll Learn

- How to create a basic FastAPI application with CRUD operations
- How to use FastMCP to convert FastAPI endpoints to MCP tools
- Two deployment patterns: standalone API vs combined API+MCP server

## Prerequisites

- Python 3.8+
- Basic knowledge of FastAPI and REST APIs

## Project Setup

### 1. Clone and Setup Environment

```bash
# Clone the repository
git clone <your-repo-url>
cd 1-mcp-server-from-any-api

# Create virtual environment (required on macOS/modern Python)
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Project Structure

```
1-mcp-server-from-any-api/
├── app/
│   ├── main.py      # FastAPI application with Todo CRUD
│   └── schemas.py   # Pydantic models
├── mcp_server.py    # Combined FastAPI + MCP server
├── requirements.txt # Project dependencies
└── README.md
```

## Part 1: The FastAPI Application

The core API is defined in `app/main.py` and provides basic Todo operations:

- **GET /api/todos** - List all todos
- **POST /api/todos** - Create a new todo
- **GET /api/todos/{id}** - Get specific todo
- **PUT /api/todos/{id}** - Update todo
- **DELETE /api/todos/{id}** - Delete todo

### Key Features:
- Uses in-memory storage (Python list) for simplicity
- Pydantic models for data validation
- Standard FastAPI patterns

### Run Standalone API

```bash
python app/main.py
```

Visit:
- API endpoints: http://localhost:8000/api/todos
- Interactive docs: http://localhost:8000/api/docs

### Test the API

```bash
# List todos (empty initially)
curl http://localhost:8000/api/todos

# Create a todo
curl -X POST http://localhost:8000/api/todos \
  -H "Content-Type: application/json" \
  -d '{"title": "Learn MCP", "description": "Complete the tutorial"}'

# List todos (now with data)
curl http://localhost:8000/api/todos

# Update todo
curl -X PUT http://localhost:8000/api/todos/1 \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'

# Delete todo
curl -X DELETE http://localhost:8000/api/todos/1
```

## Part 2: MCP Server Integration

The `mcp_server.py` file demonstrates the FastMCP integration pattern:

```python
from fastmcp import FastMCP
from app.main import api_app as todo_api

# Convert FastAPI app to MCP server
mcp = FastMCP.from_fastapi(app=todo_api, name="Todo MCP")

# Create HTTP-accessible MCP server
mcp_app = mcp.http_app(path='/mcp')

# Mount both API and MCP in combined server
app = FastAPI(title="Todo API with MCP")
app.mount("/api", todo_api)      # Original API
app.mount("/llm", mcp_app)       # MCP endpoints
```

### Run Combined Server

```bash
python mcp_server.py
```

This provides:
- **Original API**: http://localhost:8000/api/todos
- **MCP endpoints**: http://localhost:8000/llm/mcp/
- **API docs**: http://localhost:8000/api/docs
- **MCP docs**: http://localhost:8000/llm/docs

## Part 3: MCP Client Configuration

### Option 1: Stdio Transport (Recommended)

Add to your MCP client configuration:

```json
{
  "mcpServers": {
    "todo": {
      "command": "python",
      "args": ["/path/to/mcp_server.py"],
      "cwd": "/path/to/1-mcp-server-from-any-api"
    }
  }
}
```

### Option 2: HTTP Transport

First, start the server:
```bash
python mcp_server.py
```

Then configure your MCP client:
```json
{
  "mcpServers": {
    "todo": {
      "url": "http://localhost:8000/llm/mcp/",
      "transport": "http"
    }
  }
}
```

## How It Works

### FastMCP Conversion Process

1. **`FastMCP.from_fastapi(app=todo_api)`** automatically discovers all FastAPI routes
2. **Each endpoint becomes an MCP tool** with the same parameters
3. **FastAPI operation IDs** become tool names (e.g., `list_todos`, `create_todo`)
4. **Request/response schemas** are preserved from Pydantic models

### Generated MCP Tools

The FastAPI endpoints are automatically converted to these MCP tools:

- `list_todos` → GET /api/todos
- `create_todo` → POST /api/todos  
- `read_todo` → GET /api/todos/{id}
- `update_todo` → PUT /api/todos/{id}
- `delete_todo` → DELETE /api/todos/{id}

### Benefits of This Pattern

1. **Single codebase** - maintain one FastAPI app for both REST and MCP
2. **Automatic synchronization** - MCP tools always match API endpoints
3. **Flexible deployment** - choose stdio or HTTP transport
4. **Development friendly** - test REST API independently

## Next Steps

### Extending the Tutorial

1. **Add authentication** - configure FastMCP with API keys
2. **Database integration** - replace in-memory storage with SQLAlchemy
3. **Advanced routing** - customize which endpoints become MCP tools
4. **Error handling** - implement proper error responses

### Applying to Your APIs

To convert your own FastAPI application:

1. **Import your FastAPI app**: `from your_app import app`
2. **Create MCP server**: `mcp = FastMCP.from_fastapi(app=app)`
3. **Choose transport**: stdio for simplicity, HTTP for flexibility
4. **Configure client** with appropriate MCP server settings

This pattern works with any FastAPI application, making your existing APIs immediately available to AI assistants through the MCP protocol.