from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# ---- Task ----
class TaskCreate(BaseModel):
    title: str
    done: bool = False

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None

class TaskResponse(TaskCreate):
    id: int
    created_at: datetime
    class Config:
        orm_mode = True

# ---- User ----
class UserCreate(BaseModel):
    name: str
    email: str

class UserResponse(UserCreate):
    id: int
    created_at: datetime
    class Config:
        orm_mode = True

# ---- Conversation ----
class ConversationCreate(BaseModel):
    title: Optional[str] = "New Conversation"
    user_id: int

class ConversationResponse(ConversationCreate):
    id: int
    created_at: datetime
    class Config:
        orm_mode = True

# ---- Message ----
class MessageCreate(BaseModel):
    content: str
    is_bot: bool = False
    conversation_id: int

class MessageResponse(MessageCreate):
    id: int
    created_at: datetime
    class Config:
        orm_mode = True