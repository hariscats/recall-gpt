"""
User models for the AI Learning Assistant application.
"""

from datetime import datetime
from typing import Dict, List, Optional
from pydantic import BaseModel, Field, EmailStr, UUID4


class UserPreferences(BaseModel):
    """User learning preferences."""
    
    preferred_topics: List[str] = Field(
        default_factory=list,
        description="List of topics the user is interested in"
    )
    learning_pace: str = Field(
        default="medium", 
        description="Preferred learning pace (slow, medium, fast)"
    )
    notification_enabled: bool = Field(
        default=True,
        description="Whether notifications are enabled"
    )
    daily_session_goal: int = Field(
        default=20,
        description="Number of minutes the user wants to study daily"
    )
    difficulty_preference: str = Field(
        default="adaptive",
        description="Preferred difficulty level (easy, medium, hard, adaptive)"
    )


class UserProfile(BaseModel):
    """User profile information."""
    
    id: UUID4 = Field(description="Unique identifier for the user")
    email: EmailStr = Field(description="User's email address")
    username: str = Field(description="User's chosen username")
    full_name: Optional[str] = Field(None, description="User's full name")
    created_at: datetime = Field(default_factory=datetime.now, description="When the user account was created")
    last_active: datetime = Field(default_factory=datetime.now, description="When the user was last active")
    preferences: UserPreferences = Field(default_factory=UserPreferences, description="User preferences")
    topic_proficiency: Dict[str, float] = Field(
        default_factory=dict,
        description="Dictionary mapping topics to proficiency levels (0.0 to 1.0)"
    )
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "f8c3de3d-1fea-4d7c-a8b0-56f0d5a0b76c",
                "email": "user@example.com",
                "username": "learner42",
                "full_name": "Jane Doe",
                "preferences": {
                    "preferred_topics": ["machine learning", "python"],
                    "learning_pace": "medium",
                    "notification_enabled": True,
                    "daily_session_goal": 30,
                    "difficulty_preference": "adaptive"
                },
                "topic_proficiency": {
                    "python": 0.75,
                    "machine learning": 0.45
                }
            }
        }
    }


class UserProfileCreate(BaseModel):
    """Schema for creating a new user profile."""
    
    email: EmailStr = Field(description="User's email address")
    username: str = Field(description="User's chosen username")
    full_name: Optional[str] = Field(None, description="User's full name")
    preferences: Optional[UserPreferences] = Field(None, description="User preferences")


class UserProfileUpdate(BaseModel):
    """Schema for updating an existing user profile."""
    
    email: Optional[EmailStr] = Field(None, description="User's email address")
    username: Optional[str] = Field(None, description="User's chosen username")
    full_name: Optional[str] = Field(None, description="User's full name")
    preferences: Optional[UserPreferences] = Field(None, description="User preferences")