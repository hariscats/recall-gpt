"""
Learning material models for the AI Learning Assistant application.
"""

from datetime import datetime
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field, UUID4


class ContentBlock(BaseModel):
    """A block of learning content."""
    
    type: str = Field(description="Type of content block (text, code, image, etc.)")
    content: str = Field(description="Content string or reference")
    metadata: Dict[str, Any] = Field(
        default_factory=dict, 
        description="Additional metadata for the content block"
    )


class LearningMaterial(BaseModel):
    """A learning material entity."""
    
    id: UUID4 = Field(description="Unique identifier for the learning material")
    title: str = Field(description="Title of the learning material")
    description: str = Field(description="Brief description of the material")
    topics: List[str] = Field(description="Associated topics/tags")
    difficulty_level: float = Field(
        description="Difficulty level from 0.0 (easiest) to 1.0 (hardest)"
    )
    content_blocks: List[ContentBlock] = Field(description="Blocks of learning content")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    author_id: Optional[UUID4] = Field(None, description="Creator of the material")
    source_reference: Optional[str] = Field(
        None, 
        description="Reference to original source if applicable"
    )
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "a1b2c3d4-e5f6-4a5b-8c7d-9e0f1a2b3c4d",
                "title": "Introduction to Python Variables",
                "description": "Learn about variables and data types in Python",
                "topics": ["python", "programming basics"],
                "difficulty_level": 0.2,
                "content_blocks": [
                    {
                        "type": "text",
                        "content": "Variables in Python are used to store data values...",
                        "metadata": {"format": "markdown"}
                    },
                    {
                        "type": "code",
                        "content": "x = 5\ny = 'Hello'\nprint(x, y)",
                        "metadata": {"language": "python"}
                    }
                ]
            }
        }
    }


class LearningItem(BaseModel):
    """An item for learning/review in a session."""
    
    id: UUID4 = Field(description="Unique identifier for the learning item")
    material_id: UUID4 = Field(description="Reference to associated learning material")
    user_id: UUID4 = Field(description="User this item is for")
    content: str = Field(description="The primary content for this item")
    question: Optional[str] = Field(None, description="Question for active recall")
    answer: Optional[str] = Field(None, description="Answer to the question")
    context: Optional[str] = Field(None, description="Additional context for the item")
    difficulty: float = Field(
        description="Current difficulty rating for this user (0.0 to 1.0)"
    )
    next_review: datetime = Field(
        description="When this item should next be reviewed"
    )
    review_count: int = Field(
        default=0, 
        description="Number of times this item has been reviewed"
    )
    ease_factor: float = Field(
        default=2.5, 
        description="Spaced repetition ease factor"
    )
    interval_days: float = Field(
        default=1.0, 
        description="Current interval in days"
    )
    last_reviewed: Optional[datetime] = Field(
        None,
        description="When this item was last reviewed"
    )
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "b2c3d4e5-f6a7-4b5c-9d0e-1f2a3b4c5d6e",
                "material_id": "a1b2c3d4-e5f6-4a5b-8c7d-9e0f1a2b3c4d",
                "user_id": "f8c3de3d-1fea-4d7c-a8b0-56f0d5a0b76c",
                "content": "Variables in Python are used to store data values.",
                "question": "What are variables used for in Python?",
                "answer": "To store data values",
                "context": "Introduction to Python Variables",
                "difficulty": 0.3,
                "next_review": "2023-11-01T14:30:00",
                "review_count": 2,
                "ease_factor": 2.3,
                "interval_days": 4.0,
                "last_reviewed": "2023-10-28T09:15:00"
            }
        }
    }


class LearningMaterialCreate(BaseModel):
    """Schema for creating new learning material."""
    
    title: str
    description: str
    topics: List[str]
    difficulty_level: float
    content_blocks: List[ContentBlock]
    source_reference: Optional[str] = None
    
    
class LearningItemCreate(BaseModel):
    """Schema for creating a new learning item."""
    
    material_id: UUID4
    user_id: UUID4
    content: str
    question: Optional[str] = None
    answer: Optional[str] = None
    context: Optional[str] = None
    difficulty: float
    next_review: Optional[datetime] = None