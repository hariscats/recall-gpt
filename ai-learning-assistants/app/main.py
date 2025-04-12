"""
Simplified main application entry point for the AI Learning Assistant.
"""
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, Optional
import uuid

# Create FastAPI app
app = FastAPI(
    title="AI Learning Assistant",
    description="An AI-powered tool for efficient learning",
    version="0.1.0",
)

# In-memory data store for demonstration
users_db = {}
learning_materials_db = {}

# Models
class UserBase(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: str
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "f8c3de3d-1fea-4d7c-a8b0-56f0d5a0b76c",
                "username": "learner42",
                "email": "user@example.com",
                "full_name": "Jane Doe"
            }
        }
    }

# Routes
@app.get("/")
async def root():
    """Health check endpoint."""
    return {"status": "ok", "message": "AI Learning Assistant API is running"}

@app.get("/info")
async def info():
    """Basic API information."""
    return {
        "app_name": "AI Learning Assistant",
        "version": "0.1.0",
        "description": "A personalized learning system powered by AI"
    }

@app.post("/users/", response_model=User)
async def create_user(user: UserCreate):
    """Create a new user."""
    user_id = str(uuid.uuid4())
    new_user = User(
        id=user_id,
        username=user.username,
        email=user.email,
        full_name=user.full_name
    )
    users_db[user_id] = new_user
    return new_user

@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: str):
    """Get a user by ID."""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    return users_db[user_id]

@app.get("/users/")
async def list_users():
    """List all users."""
    return list(users_db.values())