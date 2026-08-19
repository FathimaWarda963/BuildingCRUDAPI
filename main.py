from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

# This creates an instance of FastAPI
app = FastAPI(
    title="Task API",
    description="A simple in-memory To-Do list API"
)

# The Pydantic Scheme Class is used in order to validate the incoming data when a task is created 
class TaskCreate(BaseModel):
    title: str

# This is a miniature storage unit within the code used to demonstrate the various endpoints
#  It acts as the database for the demonstration of this project
tasks_db = [
    {"id": 1, "title": "Sand basswood strips🪵", "done": False},
    {"id": 2, "title": "Export heavy 3D models 🧊", "done": True},
    {"id": 3, "title": "Print large-format drawings 🖼️", "done": False},
]

# Root endpoint - This acts as the API's front door and describes or demonstrates the available routes
@app.get("/")
def read_root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }

# Health check endpoint - This is used by external monitors in order to see if particular servers are available
@app.get("/health")
def health_check():
    return {"status": "ok"}

# This enables us to obtain all of the tasks available in the storage unit
@app.get("/tasks")
def get_tasks():
    return tasks_db

# This enables us to view the details of a task by using their id 
@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks_db:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

# This endpoint enables us to create data by "sending" the information "posted" into the server
@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate):
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