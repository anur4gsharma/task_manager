from fastapi import FastAPI, HTTPException
from starlette import status

from app.schemas import TaskCreate, TaskResponse, TaskUpdate
from app.tasks import create_task, find_task, list_tasks

app = FastAPI(title="Task Manager API", version="0.1.0")


@app.get("/")
def root():
    return {"message": "welcome"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/tasks", response_model=list[TaskResponse])
def get_tasks(completed: bool | None = None):

    return list_tasks(completed)

@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task_by_id(task_id : int):

    output = find_task(task_id)

    if output is None:
        raise HTTPException(status_code=404, detail=f"Task with id = {task_id} not found.")

    return output

@app.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_tasks(task: TaskCreate):

    output = create_task(task.description)

    return output

@app.put("/tasks", response_model=TaskResponse)
def update_task(task: TaskUpdate)