"""Tiny FastAPI app for the MCP tutorial."""

from fastapi import FastAPI, HTTPException
from typing import List

try:
    from app import schemas
except ImportError:
    # When running directly from app/ directory
    import schemas

# Create the main API app
api_app = FastAPI(title="Todo API")

# In-memory storage
todos_db: List[schemas.Todo] = []
next_id = 1


@api_app.get("/")
async def root():
    return {"message": "Todo API running"}


@api_app.get("/todos", response_model=List[schemas.Todo])
async def list_todos():
    return todos_db


@api_app.post("/todos", response_model=schemas.Todo)
async def create_todo(todo: schemas.TodoCreate):
    global next_id
    new_todo = schemas.Todo(
        id=next_id,
        title=todo.title,
        description=todo.description,
        completed=todo.completed
    )
    todos_db.append(new_todo)
    next_id += 1
    return new_todo


@api_app.get("/todos/{todo_id}", response_model=schemas.Todo)
async def read_todo(todo_id: int):
    for todo in todos_db:
        if todo.id == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")


@api_app.put("/todos/{todo_id}", response_model=schemas.Todo)
async def update_todo(todo_id: int, todo_update: schemas.TodoUpdate):
    for i, todo in enumerate(todos_db):
        if todo.id == todo_id:
            update_data = todo_update.dict(exclude_unset=True)
            updated_todo = todo.copy(update=update_data)
            todos_db[i] = updated_todo
            return updated_todo
    raise HTTPException(status_code=404, detail="Todo not found")


@api_app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int):
    for i, todo in enumerate(todos_db):
        if todo.id == todo_id:
            todos_db.pop(i)
            return {"message": "Todo deleted"}
    raise HTTPException(status_code=404, detail="Todo not found")


# Create the main app and mount the API
app = FastAPI(title="Todo API Server")

@app.get("/")
async def main_root():
    return {
        "message": "Todo API Server",
        "endpoints": {
            "api": "http://localhost:8000/api/todos",
            "api_docs": "http://localhost:8000/api/docs"
        }
    }

# Mount the API app at /api
app.mount("/api", api_app)


if __name__ == "__main__":
    import uvicorn
    print("Starting standalone FastAPI Todo API...")
    print("API endpoints: http://localhost:8000/api/todos")
    print("API docs: http://localhost:8000/api/docs")
    print("Root: http://localhost:8000/")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)