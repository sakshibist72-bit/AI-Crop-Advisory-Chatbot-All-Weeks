
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional


router = APIRouter()

# --- Data model (like a blueprint for a task) ---
class Task(BaseModel):
    title: str
    done: bool = False

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None

# --- In-memory "database" (just a list for now) ---
tasks = [
    {"id": 1, "title": "Buy groceries", "done": False},
    {"id": 2, "title": "Do laundry", "done": True},
]
next_id = 3


# 1. GET /api/tasks — list all tasks
@router.get("/")
def get_all_tasks():
    return tasks


# 2. GET /api/tasks/search?q=... — search tasks
@router.get("/search")
def search_tasks(q: str = ""):
    results = [t for t in tasks if q.lower() in t["title"].lower()]
    return results


# 3. GET /api/tasks/{task_id} — get one task
@router.get("/{task_id}")
def get_task(task_id: int):
    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


# 4. POST /api/tasks — create a task
@router.post("/", status_code=201)
def create_task(task: Task):
    global next_id
    new_task = {"id": next_id, "title": task.title, "done": task.done}
    next_id += 1
    tasks.append(new_task)
    return new_task


# 5. PUT /api/tasks/{task_id} — update a task
@router.put("/{task_id}")
def update_task(task_id: int, updates: TaskUpdate):
    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if updates.title is not None:
        task["title"] = updates.title
    if updates.done is not None:
        task["done"] = updates.done
    return task


# 6. DELETE /api/tasks/{task_id} — delete a task
@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: int):
    global tasks
    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    tasks = [t for t in tasks if t["id"] != task_id]
