"""
Analytics models for the AI Learning Assistant application.
"""
from datetime import datetime, date
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field, UUID4

class TopicPerformance(BaseModel):
    """Performance metrics for a specific topic."""
    
    topic: str = Field(description="Topic name")
    proficiency: float = Field(
        description="Overall proficiency score (0.0 to 1.0)"
    )
    items_studied: int = Field(description="Number of items studied in this topic")
    average_accuracy: float = Field(description="Average accuracy on questions")
    average_response_time_ms: int = Field(
        description="Average response time in milliseconds"
    )
    retention_rate: float = Field(
        description="Percentage of items retained over time"
    )
    last_studied: datetime = Field(description="When the topic was last studied")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "topic": "python",
                "proficiency": 0.78,
                "items_studied": 42,
                "average_accuracy": 0.85,
                "average_response_time_ms": 2300,
                "retention_rate": 0.72,
                "last_studied": "2023-10-31T14:30:00"
            }
        }
    }

class DailyStats(BaseModel):
    """Learning statistics for a specific day."""
    
    date: date = Field(description="The date for these statistics")
    total_time_spent_minutes: int = Field(description="Total time spent learning")
    items_studied: int = Field(description="Number of items reviewed")
    new_items_learned: int = Field(description="Number of new items introduced")
    accuracy_rate: float = Field(description="Percentage of correct responses")
    topics_studied: List[str] = Field(description="Topics studied on this day")
    streaks: Dict[str, int] = Field(
        description="Current streak counters for various metrics"
    )
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "date": "2023-11-01",
                "total_time_spent_minutes": 35,
                "items_studied": 25,
                "new_items_learned": 8,
                "accuracy_rate": 0.82,
                "topics_studied": ["python", "data structures"],
                "streaks": {
                    "daily_practice": 5,
                    "perfect_sessions": 2
                }
            }
        }
    }

class LearningProgress(BaseModel):
    """Progress tracking for a user's learning journey."""
    
    user_id: UUID4 = Field(description="User ID")
    global_proficiency: float = Field(
        description="Overall proficiency across all topics"
    )
    total_time_spent_hours: float = Field(description="Total learning time in hours")
    total_items_learned: int = Field(description="Total learning items completed")
    retention_rate: float = Field(
        description="Overall retention rate across all topics"
    )
    topic_progression: Dict[str, float] = Field(
        description="Map of topic to proficiency level"
    )
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "user_id": "f8c3de3d-1fea-4d7c-a8b0-56f0d5a0b76c",
                "global_proficiency": 0.68,
                "total_time_spent_hours": 12.5,
                "total_items_learned": 150,
                "retention_rate": 0.75,
                "topic_progression": {
                    "python": 0.85,
                    "data structures": 0.72,
                    "algorithms": 0.65,
                    "machine learning": 0.45
                }
            }
        }
    }

class PerformanceMetrics(BaseModel):
    """Comprehensive performance metrics for a user."""
    
    user_id: UUID4 = Field(description="User ID")
    overall_progress: LearningProgress = Field(
        description="Overall learning progress"
    )
    topic_performance: Dict[str, TopicPerformance] = Field(
        default_factory=dict,
        description="Map of topic to performance metrics"
    )
    daily_stats: Dict[str, DailyStats] = Field(
        default_factory=dict,
        description="Map of date string (YYYY-MM-DD) to daily statistics"
    )
    learning_curve: Dict[str, List[float]] = Field(
        default_factory=dict,
        description="Map of topic to proficiency measurements over time"
    )
    recommendations: Dict[str, Any] = Field(
        default_factory=dict,
        description="Personalized learning recommendations"
    )
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "user_id": "f8c3de3d-1fea-4d7c-a8b0-56f0d5a0b76c",
                "overall_progress": {
                    "user_id": "f8c3de3d-1fea-4d7c-a8b0-56f0d5a0b76c",
                    "global_proficiency": 0.68,
                    "total_time_spent_hours": 12.5,
                    "total_items_learned": 150,
                    "retention_rate": 0.75,
                    "topic_progression": {
                        "python": 0.85,
                        "data structures": 0.72
                    }
                },
                "topic_performance": {
                    "python": {
                        "topic": "python",
                        "proficiency": 0.85,
                        "items_studied": 65,
                        "average_accuracy": 0.88,
                        "average_response_time_ms": 1950,
                        "retention_rate": 0.82,
                        "last_studied": "2023-11-01T10:00:00"
                    }
                },
                "recommendations": {
                    "focus_topics": ["algorithms", "machine learning"],
                    "review_needed": ["data structures"],
                    "suggested_pace": "medium"
                }
            }
        }
    }