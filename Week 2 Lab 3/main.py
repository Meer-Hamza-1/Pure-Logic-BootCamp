from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI()

# Data store
todos = []
next_id = 1

# Models
class TodoCreate(BaseModel):
    title: str

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    completed: Optional[bool] = None

class TodoResponse(BaseModel):
    id: int
    title: str
    completed: bool

# POST - Add task
@app.post("/todos", response_model=TodoResponse, status_code=201)
async def create_todo(todo: TodoCreate):
    global next_id
    new_todo = {
        "id": next_id,
        "title": todo.title,
        "completed": False
    }
    todos.append(new_todo)
    next_id += 1
    return new_todo

# GET - All tasks
@app.get("/todos", response_model=List[TodoResponse])
async def get_all_todos():
    return todos

# GET - Specific task
@app.get("/todos/{id}", response_model=TodoResponse)
async def get_todo(id: int):
    todo = next((t for t in todos if t["id"] == id), None)
    if todo is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return todo

# PUT - Update task
@app.put("/todos/{id}", response_model=TodoResponse)
async def update_todo(id: int, todo_update: TodoUpdate):
    todo = next((t for t in todos if t["id"] == id), None)
    if todo is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if todo_update.title is not None:
        todo["title"] = todo_update.title
    if todo_update.completed is not None:
        todo["completed"] = todo_update.completed
    
    return todo

# DELETE - Delete task
@app.delete("/todos/{id}")
async def delete_todo(id: int):
    global todos
    todo = next((t for t in todos if t["id"] == id), None)
    if todo is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    todos = [t for t in todos if t["id"] != id]
    return {"message": "Task deleted successfully"}

@app.get("/")
async def root():
    return {
        "message": "To-Do List API",
        "docs": "/docs"
    }