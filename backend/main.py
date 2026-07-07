# main.py
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import engine, Base, get_db
import models, schemas

app = FastAPI()
Base.metadata.create_all(bind=engine)

# Allow the Vite frontend (localhost:5173) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------- TASKS ----------------

@app.get("/api/tasks", response_model=list[schemas.TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    return db.query(models.Task).all()


@app.post("/api/tasks", response_model=schemas.TaskResponse)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    db_task = models.Task(title=task.title, done=task.done)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


@app.put("/api/tasks/{task_id}", response_model=schemas.TaskResponse)
def update_task(task_id: int, updated: schemas.TaskUpdate, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if updated.title is not None:
        task.title = updated.title
    if updated.done is not None:
        task.done = updated.done
    db.commit()
    db.refresh(task)
    return task


@app.delete("/api/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"message": "Task deleted"}


# ---------------- USERS ----------------

@app.post("/users", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.get("/users", response_model=list[schemas.UserResponse])
def get_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()


@app.get("/users/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# ---------------- CONVERSATIONS ----------------

@app.post("/conversations", response_model=schemas.ConversationResponse)
def create_conversation(conv: schemas.ConversationCreate, db: Session = Depends(get_db)):
    db_conv = models.Conversation(title=conv.title, user_id=conv.user_id)
    db.add(db_conv)
    db.commit()
    db.refresh(db_conv)
    return db_conv


@app.get("/conversations", response_model=list[schemas.ConversationResponse])
def get_conversations(db: Session = Depends(get_db)):
    return db.query(models.Conversation).all()


@app.get("/conversations/{conversation_id}", response_model=schemas.ConversationResponse)
def get_conversation(conversation_id: int, db: Session = Depends(get_db)):
    conv = db.query(models.Conversation).filter(models.Conversation.id == conversation_id).first()
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conv


@app.put("/conversations/{conversation_id}", response_model=schemas.ConversationResponse)
def update_conversation(conversation_id: int, updated: schemas.ConversationCreate, db: Session = Depends(get_db)):
    conv = db.query(models.Conversation).filter(models.Conversation.id == conversation_id).first()
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    conv.title = updated.title
    conv.user_id = updated.user_id
    db.commit()
    db.refresh(conv)
    return conv


@app.delete("/conversations/{conversation_id}")
def delete_conversation(conversation_id: int, db: Session = Depends(get_db)):
    conv = db.query(models.Conversation).filter(models.Conversation.id == conversation_id).first()
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    db.delete(conv)
    db.commit()
    return {"message": "Conversation deleted"}


# ---------------- MESSAGES ----------------

@app.post("/messages", response_model=schemas.MessageResponse)
def create_message(msg: schemas.MessageCreate, db: Session = Depends(get_db)):
    db_msg = models.Message(
        content=msg.content,
        is_bot=msg.is_bot,
        conversation_id=msg.conversation_id,
    )
    db.add(db_msg)
    db.commit()
    db.refresh(db_msg)
    return db_msg


@app.get("/conversations/{conversation_id}/messages", response_model=list[schemas.MessageResponse])
def get_messages(conversation_id: int, db: Session = Depends(get_db)):
    return db.query(models.Message).filter(models.Message.conversation_id == conversation_id).all()


@app.delete("/messages/{message_id}")
def delete_message(message_id: int, db: Session = Depends(get_db)):
    msg = db.query(models.Message).filter(models.Message.id == message_id).first()
    if not msg:
        raise HTTPException(status_code=404, detail="Message not found")
    db.delete(msg)
    db.commit()
    return {"message": "Message deleted"}