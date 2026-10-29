from typing import Annotated

from pydantic import BaseModel, StringConstraints


class TaskResponse(BaseModel):
    task_id: int
    description: str
    completed: bool

class TaskCreate(BaseModel):
    description: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]

class TaskUpdate(BaseModel):
    