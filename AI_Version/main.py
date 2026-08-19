from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Task(BaseModel):
    title: str
    done: bool = False

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None

tasks_db = []

@app.get("/")
def root():
    return {"message": "Task API"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/tasks")
def get_tasks(done: Optional[bool] = None, search: Optional[str] = None):
    res = tasks_db
    if done is not None:
        res = [t for t in res if t["done"] == done]
    if search:
        res = [t for t in res if search.lower() in t["title"].lower()]
    return res

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks_db:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail="Not found")

@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(task: Task):
    if not task.title:
        raise HTTPException(status_code=400, detail="Invalid title")
    new_id = len(tasks_db) + 1
    item = {"id": new_id, "title": task.title, "done": task.done}
    tasks_db.append(item)
    return item

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task_update: TaskUpdate):
    for task in tasks_db:
        if task["id"] == task_id:
            if task_update.title is not None:
                task["title"] = task_update.title
            if task_update.done is not None:
                task["done"] = task_update.done
            return task
    raise HTTPException(status_code=404, detail="Not found")

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    for i, task in enumerate(tasks_db):
        if task["id"] == task_id:
            tasks_db.pop(i)
            return
    raise HTTPException(status_code=404, detail="Not found")