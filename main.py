from fastapi import FastAPI

# This creates an instance of FastAPI
app = FastAPI(
    title="Task API",
    description="A simple in-memory To-Do list API"
)

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