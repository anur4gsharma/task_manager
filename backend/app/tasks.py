tasks = [
    {
        "task_id": 1,
        "description": "xyz",
        "completed": True
    },
    {
        "task_id": 2,
        "description": "abc",
        "completed": False
    },
    {
        "task_id": 3,
        "description": "pqr",
        "completed": True
    },
    {
        "task_id": 4,
        "description": "efg",
        "completed": False
    },
]

def find_task(task_id: int):
    for task in tasks:
        if task["task_id"] == task_id:
            return task

    return None


def list_tasks(completed: bool | None = None):
    if completed is None:
        return tasks

    return [
        task for task in tasks
        if task["completed"] == completed
    ]

def create_task(description):

    new_task_id = tasks[-1]["task_id"] + 1

    created_task = {
        "task_id": new_task_id,
        "description": description,
        "completed": False
    }

    tasks.append(created_task)

    return created_task
