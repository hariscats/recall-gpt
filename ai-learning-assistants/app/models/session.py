"""
Session models for the AI Learning Assistant application.
"""

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field, UUID4


class SessionType(str, Enum):
    """Types of learning sessions."""
    
    NEW_CONTENT = "new_content"  # Learning new material
    REVIEW = "review"  # Reviewing previously learned material
    MIXED = "mixed"  # Combination of new and review


class SessionStatus(str, Enum):
    """Status of a learning session."""
    
    ACTIVE = "active"  # Session is ongoing
    COMPLETED = "completed"  # Session is finished
    PAUSED = "paused"  # Session is paused


class ResponseQuality(int, Enum):
    """Quality of user's response based on SM-2 algorithm."""
    
    INCORRECT = 0  # Complete blackout
    INCORRECT_REMEMBERED = 1  # Wrong answer but remembered when shown
    DIFFICULT = 2  # Correct answer but with difficulty
    CORRECT_HESITANT = 3  # Correct answer with hesitation
    CORRECT = 4  # Correct answer with good recall
    PERFECT = 5  # Perfect recall


class QuestionType(str, Enum):
    """Types of questions that can be generated."""
    
    MULTIPLE_CHOICE = "multiple_choice"
    FREE_RESPONSE = "free_response"
    FILL_IN_BLANK = "fill_in_blank"
    TRUE_FALSE = "true_false"
    CODE_COMPLETION = "code_completion"


class SessionRequest(BaseModel):
    """Request to start or continue a learning session."""
    
    user_id: UUID4 = Field(description="User ID for the session")
    session_type: SessionType = Field(description="Type of session to create")
    topic_filter: Optional[List[str]] = Field(
        None,
        description="Optional list of topics to focus on"
    )
    duration_minutes: Optional[int] = Field(
        None,
        description="Desired duration in minutes"
    )
    item_count: Optional[int] = Field(
        None,
        description="Desired number of items to review"
    )
    difficulty_range: Optional[Dict[str, float]] = Field(
        None,
        description="Min/max difficulty, e.g. {'min': 0.3, 'max': 0.7}"
    )
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "user_id": "f8c3de3d-1fea-4d7c-a8b0-56f0d5a0b76c",
                "session_type": "mixed",
                "topic_filter": ["python", "data structures"],
                "duration_minutes": 20,
                "difficulty_range": {"min": 0.2, "max": 0.8}
            }
        }
    }


class Question(BaseModel):
    """A question for active recall practice."""
    
    id: UUID4 = Field(description="Unique identifier for the question")
    item_id: UUID4 = Field(description="Associated learning item ID")
    text: str = Field(description="Question text")
    type: QuestionType = Field(description="Type of question")
    options: Optional[List[str]] = Field(
        None,
        description="Options for multiple choice questions"
    )
    correct_answer: str = Field(description="Correct answer")
    explanation: Optional[str] = Field(
        None,
        description="Explanation of the answer"
    )
    hint: Optional[str] = Field(None, description="Optional hint")
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional metadata"
    )


class UserAnswer(BaseModel):
    """User's answer to a question."""
    
    question_id: UUID4 = Field(description="ID of the question")
    answer: str = Field(description="User's answer")
    response_time_ms: int = Field(description="Time taken to answer in milliseconds")
    self_evaluation: Optional[ResponseQuality] = Field(
        None,
        description="User's self-assessment of their answer quality"
    )


class LearningFeedback(BaseModel):
    """Feedback on a user's answer."""
    
    question_id: UUID4 = Field(description="Question ID")
    is_correct: bool = Field(description="Whether the answer was correct")
    quality: ResponseQuality = Field(description="Quality assessment of response")
    explanation: str = Field(description="Explanation of the correct answer")
    next_steps: Optional[str] = Field(
        None,
        description="Suggested next steps for learning"
    )
    updated_difficulty: float = Field(description="New difficulty assessment")
    next_review_interval: float = Field(
        description="Recommended days until next review"
    )


class Session(BaseModel):
    """A learning session."""
    
    id: UUID4 = Field(description="Unique session identifier")
    user_id: UUID4 = Field(description="User ID")
    type: SessionType = Field(description="Type of session")
    status: SessionStatus = Field(description="Current status")
    started_at: datetime = Field(description="When session started")
    completed_at: Optional[datetime] = Field(None, description="When session ended")
    items: List[UUID4] = Field(description="Learning item IDs in this session")
    current_item_index: int = Field(default=0, description="Current position in items")
    results: Dict[str, LearningFeedback] = Field(
        default_factory=dict,
        description="Map of item_id to feedback"
    )
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "c3d4e5f6-a7b8-4c5d-9e0f-1a2b3c4d5e6f",
                "user_id": "f8c3de3d-1fea-4d7c-a8b0-56f0d5a0b76c",
                "type": "mixed",
                "status": "active",
                "started_at": "2023-11-01T10:00:00",
                "items": [
                    "b2c3d4e5-f6a7-4b5c-9d0e-1f2a3b4c5d6e",
                    "d4e5f6a7-b8c9-4d0e-1f2a-3b4c5d6e7f8a"
                ],
                "current_item_index": 0
            }
        }
    }


class RequestResult(BaseModel):
    """Result from a learning session request."""
    
    session_id: UUID4 = Field(description="ID of the created or continued session")
    current_question: Optional[Question] = Field(
        None,
        description="Current question if available"
    )
    session_stats: Dict[str, Any] = Field(
        description="Statistics about the session"
    )
    next_steps: str = Field(
        description="Description of what to do next"
    )