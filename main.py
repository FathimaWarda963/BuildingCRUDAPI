from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel
from typing import Optional

# This creates an instance of FastAPI
app = FastAPI(
    title="Task API",
    description="A simple in-memory To-Do list API"
)

# The Pydantic Scheme Class is used in order to validate the incoming data when a task is created 
class TaskCreate(BaseModel):
    title: str

# This is the Pydantic model used in order to keep the structure of the tasks consistent when updating 
class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None

# Initial seed data used for resets
INITIAL_TASKS = [
    {"id": 1, "title": "Sand basswood strips🪵", "done": False},
    {"id": 2, "title": "Export heavy 3D models 🧊", "done": True},
    {"id": 3, "title": "Print large-format drawings 🖼️", "done": False},
]

# This is a miniature storage unit within the code used to demonstrate the various endpoints
# It acts as the database for the demonstration of this project
tasks_db = [task.copy() for task in INITIAL_TASKS]

@app.get("/")
def read_root():
    """ROOT ENDPOINT: This acts as the API's front door and describes or demonstrates the available routes🚪"""
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks", "/stats", "/reset"]
    }

@app.get("/health")
def health_check():
    """HEALTH CHECK ENDPOINT: This used by external monitors in order to see if particular servers are available 🩺"""
    return {"status": "ok"}

@app.get("/stats")
def get_stats():
    """STATS ENDPOINT: Calculates live task metrics directly from memory 📊"""
    total = len(tasks_db)
    done_count = sum(1 for task in tasks_db if task["done"])
    return {
        "total": total,
        "done": done_count,
        "open": total - done_count
    }

@app.post("/reset")
def reset_database():
    """RESET ENDPOINT: Restores the storage unit back to the 3 initial example tasks 🔄"""
    global tasks_db
    tasks_db = [task.copy() for task in INITIAL_TASKS]
    return {"message": "Storage reset to initial example tasks"}

@app.get("/tasks")
def get_tasks(done: Optional[bool] = None, search: Optional[str] = None):
    """This enables us to obtain tasks, with optional filtering by status (?done=true) or searching titles (?search=word) 📦"""
    results = tasks_db
    if done is not None:
        results = [t for t in results if t["done"] == done]
    if search is not None:
        results = [t for t in results if search.lower() in t["title"].lower()]
    return results

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    """This enables us to view the details of a task by using their id 🪪"""
    for task in tasks_db:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate):
    """This endpoint enables us to create data by "sending" the information "posted" into the server💬"""
    # This validates the incoming information, such that if the title is empty, it is not allowed
    if not task.title or not task.title.strip():
        raise HTTPException(
            status_code=400, 
            detail="Title cannot be empty or blank"
        )
    
    # This automatically increments the id so that the new information is assigned a unique value 
    next_id = max([t["id"] for t in tasks_db], default=0) + 1
    
    # This then gives the new task the structure required to be added into the storage unit
    new_task = {
        "id": next_id,
        "title": task.title.strip(),
        "done": False
    }
    
    # Finally, the task is added to our storage unit
    tasks_db.append(new_task)
    return new_task

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task_update: TaskUpdate):
    """This endpoint enables us to update a particular task within the storage unit using their id for search 🛠️"""
    for task in tasks_db:
        if task["id"] == task_id:
            # This is to ensure that the user provides the title to keep the structure consistent
            if task_update.title is not None:
                if not task_update.title.strip():
                    raise HTTPException(status_code=400, detail="Title cannot be empty or blank")
                task["title"] = task_update.title.strip()
            
            # This is to update the completion status of the task if provided 
            if task_update.done is not None:
                task["done"] = task_update.done
                
            return task

    # If the id is not found, then an exception is raised, along with 404 error code
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    """This endpoint enables us to delete a task from the storage unit using their id for search 🗑️"""
    for index, task in enumerate(tasks_db):
        if task["id"] == task_id:
            tasks_db.pop(index)
            # This particular code number returns an empty body as output
            return Response(status_code=status.HTTP_204_NO_CONTENT)
            
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")