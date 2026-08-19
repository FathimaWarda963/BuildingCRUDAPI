# Task API — Building CRUD API 🚀
A lightweight, in-memory RESTful To-Do list API built with **FastAPI**, **Pydantic**, and **Uvicorn**.



## 📖 API Interactive Documentation

### Swagger UI Overview 
![Swagger UI Overview](./SwaggerUI_Overview.png)


### 🛠️ How to Install & Run
1. **Clone the repository:**
   ```bash
   git clone <https://github.com/FathimaWarda963/BuildingCRUDAPI>
   cd BuildingCRUDAPI


### Install Dependencies 
pip install fastapi uvicorn pydantic


### Run the server 
uvicorn main:app --reload


### Access Swagger UI: 
Open http://127.0.0.1:8000/docs in your browser. 


### API Endpoints
__________________________________________________________________________________________________________
| Method     | Endpoint           | Description                           | Status Code                   |
|------------|--------------------|---------------------------------------|-------------------------------|
| **GET**    | `/`                | Root endpoint displaying API metadata | 200 OK                        |
| **GET**    | `/health`          | Server health check monitor           | 200 OK                        |
| **GET**    | `/tasks`           | Retrieve all tasks from storage       | 200 OK                        |
| **GET**    | `/tasks/{task_id}` | Fetch a single task by ID             | 200 OK / 404 Not Found        |
| **POST**   | `/tasks`           | Create a new task (requires title)    | 201 Created / 400 Bad Request |
| **PUT**    | `/tasks/{task_id}` | Update task title or done status      | 200 OK / 400 / 404            |
| **DELETE** | `/tasks/{task_id}` | Remove a task by ID                   | 204 No Content / 404          |
|____________|____________________|_______________________________________|_______________________________|


### Sample curl -i Execution Output 
Testing Single Task Retrieval with curl -i http://127.0.0.1:8000/tasks/1  

HTTP/1.1 200 OK  

date: Wed, 19 Aug 2026 00:28:59 GMT  

server: uvicorn  

content-length: 56  

content-type: application/json

{"id":1,"title":"Sand basswood strips🪵","done":false}


## 🧪 The Mortality Experiment

When custom tasks are added via `POST /tasks` and the Uvicorn server process is restarted, all dynamically created tasks vanish, reverting the database back to the initial seed array. This happens because Python list storage resides purely in volatile RAM; once the execution process terminates, memory is wiped cleanly.


## 🤖 Stage 7 — AI vs Me

### Prompt Used:
"Build a RESTful To-Do list API using FastAPI and Pydantic with in-memory storage. Include endpoints for GET /, GET /health, GET /tasks (supporting query filtering for 'done' and 'search'), GET /tasks/{id}, POST /tasks (201 Created, requires non-empty title), PUT /tasks/{id}, and DELETE /tasks/{id} (204 No Content). Handle 400 Bad Request for blank titles and 404 for missing IDs."

### Code Review & Comparison:
1. **What the AI tool did better:** The AI simplified optional query parameter default declarations in `GET /tasks` without needing redundant local assignment wrappers.
2. **What the AI tool got wrong:** The AI used `len(tasks_db) + 1` for ID assignment instead of tracking maximum existing IDs (`max(id) + 1`). Deleting item `1` and adding a new task creates duplicate IDs.
3. **What the prompt forgot to specify:** The prompt did not specify string whitespace handling (`.strip()`), causing the AI to allow whitespace-only titles like `"   "` through validation.

### Rematch Improvement:
- **Updated Prompt Addition:** *"Ensure auto-incrementing IDs account for deleted items, and trim string inputs using .strip() to reject whitespace-only titles."*
- **Result:** The regenerated code accurately sanitized empty title strings and maintained unique ID sequences across deletions.
