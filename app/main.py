from fastapi import FastAPI, HTTPException, Header, Depends
from pydantic import BaseModel
from typing import Optional
import uuid

app = FastAPI()
todos = {}
TOKEN = "test-token"

class TodoCreate(BaseModel):
    title: str
    completed: bool = False

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    completed: Optional[bool] = None

def verify_token(authorization: str = Header(None)):
    if authorization != f"Bearer {TOKEN}":
        raise HTTPException(status_code=401, detail="Unauthorized")

@app.post("/todos", status_code=201)
def create_todo(todo: TodoCreate, _: None = Depends(verify_token)):
    todo_id = str(uuid.uuid4())
    item = {"id": todo_id, "title": todo.title, "completed": todo.completed}
    todos[todo_id] = item
    return item

@app.get("/todos/{todo_id}")
def get_todo(todo_id: str, _: None = Depends(verify_token)):
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail="Not found")
    return todos[todo_id]

@app.get("/todos")
def list_todos(_: None = Depends(verify_token)):
    return list(todos.values())

@app.put("/todos/{todo_id}")
def update_todo(todo_id: str, todo: TodoUpdate, _: None = Depends(verify_token)):
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail="Not found")
    if todo.title is not None:
        todos[todo_id]["title"] = todo.title
    if todo.completed is not None:
        todos[todo_id]["completed"] = todo.completed
    return todos[todo_id]

@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: str, _: None = Depends(verify_token)):
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail="Not found")
    del todos[todo_id]