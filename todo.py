from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel

app = FastAPI()

#root 
@app.get('/')
def root():
    return "This is a todo app"

Todos = {
    1: {
        "title": "2CC course",
        "completed": False,
    },
    2: {
        "title": "2CC course Report",
        "completed": False,
    }
}

class TodoItem(BaseModel):
    title: str
    completed: bool

@app.get("/todos", status_code=status.HTTP_200_OK)
def get_all_todo_items(title: str =""):
    results = {}
    
    if title != "" or title != None:
        for id in Todos:
            if title in Todos[id]["title"]:
                results[id] = Todos[id]
    else:
        results = Todos
    
    return results

@app.get("/todos", status_code=status.HTTP_200_OK)
def get_todo_item(id: int):
    if id in Todos:
        return Todos[id]
    
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")


@app.get("/todos", status_code=status.HTTP_201_CREATED)
def create_todo_item(todo_item: TodoItem):
    id = max(Todos)+1
    Todos[id] = todo_item.dict()
    return Todos[id]


@app.get("/todos/{id}", status_code=status.HTTP_200_OK)
def update_todo_item(id: int, todo_item: TodoItem):
    if id in Todos:
        Todos[id] = todo_item.dict()
        return Todos[id]
    
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

@app.delete("/todos/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo_item(id: int):
    if id in Todos:
        Todos.pop(id)
        return
    
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")