from fastapi import FastAPI, HTTPException

# This creates an instance of FastAPI
app = FastAPI(
    title="Task API",
    description="A simple in-memory To-Do list API"
)

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
    # First we use loops to go through each of the tasks and if a match is found, that particular task is returned
    for task in tasks_db:
        if task["id"] == task_id:
            return task
            
    # If the id is not found, then an exception is raised, along with 404 error code, and an easy to understand 
    # error message 
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")