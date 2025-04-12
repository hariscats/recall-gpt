"""
Scheduling models for the AI Learning Assistant's spaced repetition system.
"""

from datetime import datetime, date
from typing import Dict, List, Optional
from pydantic import BaseModel, Field, UUID4


class ScheduleItem(BaseModel):
    """An item scheduled for review."""
    
    item_id: UUID4 = Field(description="ID of the learning item")
    user_id: UUID4 = Field(description="User ID")
    due_date: datetime = Field(description="When the item is due for review")
    priority: float = Field(description="Priority score (higher means more important)")
    estimated_time_seconds: int = Field(description="Estimated time to review in seconds")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "item_id": "b2c3d4e5-f6a7-4b5c-9d0e-1f2a3b4c5d6e",
                "user_id": "f8c3de3d-1fea-4d7c-a8b0-56f0d5a0b76c",
                "due_date": "2023-11-02T15:00:00",
                "priority": 0.85,
                "estimated_time_seconds": 60
            }
        }
    }


class DailySchedule(BaseModel):
    """Schedule for a specific date."""
    
    schedule_date: date = Field(description="The date this schedule is for")
    user_id: UUID4 = Field(description="User ID")
    items: List[UUID4] = Field(description="Items scheduled for review")
    total_items: int = Field(description="Total number of items")
    estimated_time_minutes: int = Field(description="Estimated time in minutes")
    new_items_count: int = Field(description="Number of new items introduced")
    review_items_count: int = Field(description="Number of review items")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "schedule_date": "2023-11-02",
                "user_id": "f8c3de3d-1fea-4d7c-a8b0-56f0d5a0b76c",
                "items": [
                    "b2c3d4e5-f6a7-4b5c-9d0e-1f2a3b4c5d6e",
                    "d4e5f6a7-b8c9-4d0e-1f2a-3b4c5d6e7f8a"
                ],
                "total_items": 2,
                "estimated_time_minutes": 5,
                "new_items_count": 1,
                "review_items_count": 1
            }
        }
    }


class Schedule(BaseModel):
    """A user's learning schedule."""
    
    user_id: UUID4 = Field(description="User ID")
    daily_schedules: Dict[str, DailySchedule] = Field(
        default_factory=dict,
        description="Map of date string (YYYY-MM-DD) to daily schedule"
    )
    total_items_due: int = Field(
        description="Total number of items due across all days"
    )
    overdue_items_count: int = Field(
        default=0,
        description="Number of overdue items"
    )
    upcoming_items_count: int = Field(
        default=0,
        description="Number of upcoming items in next 7 days"
    )
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "user_id": "f8c3de3d-1fea-4d7c-a8b0-56f0d5a0b76c",
                "daily_schedules": {
                    "2023-11-02": {
                        "schedule_date": "2023-11-02",
                        "user_id": "f8c3de3d-1fea-4d7c-a8b0-56f0d5a0b76c",
                        "items": [
                            "b2c3d4e5-f6a7-4b5c-9d0e-1f2a3b4c5d6e"
                        ],
                        "total_items": 1,
                        "estimated_time_minutes": 3,
                        "new_items_count": 0,
                        "review_items_count": 1
                    },
                    "2023-11-03": {
                        "schedule_date": "2023-11-03",
                        "user_id": "f8c3de3d-1fea-4d7c-a8b0-56f0d5a0b76c",
                        "items": [
                            "d4e5f6a7-b8c9-4d0e-1f2a-3b4c5d6e7f8a"
                        ],
                        "total_items": 1,
                        "estimated_time_minutes": 2,
                        "new_items_count": 1,
                        "review_items_count": 0
                    }
                },
                "total_items_due": 2,
                "overdue_items_count": 0,
                "upcoming_items_count": 2
            }
        }
    }


class ScheduleRequest(BaseModel):
    """Request to generate or refresh a schedule."""
    
    user_id: UUID4 = Field(description="User ID")
    from_date: Optional[date] = Field(
        None,
        description="Start date (defaults to today)"
    )
    days: Optional[int] = Field(
        7,
        description="Number of days to schedule (default 7)"
    )
    max_daily_items: Optional[int] = Field(
        None,
        description="Maximum items per day (defaults to user preference)"
    )
    topic_filter: Optional[List[str]] = Field(
        None,
        description="Optional list of topics to focus scheduling on"
    )
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "user_id": "f8c3de3d-1fea-4d7c-a8b0-56f0d5a0b76c",
                "from_date": "2023-11-01",
                "days": 14,
                "max_daily_items": 20,
                "topic_filter": ["python", "machine learning"]
            }
        }
    }