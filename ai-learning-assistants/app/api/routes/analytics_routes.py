"""
Analytics routes for the AI Learning Assistant API.
"""

import logging
import uuid
from datetime import date
from typing import Dict, Any, List, Optional

from fastapi import APIRouter, HTTPException, Depends, status, Query
from opentelemetry import trace

from app.models.analytics import PerformanceMetrics, TopicPerformance, DailyStats

# Setup router and tracer
router = APIRouter()
tracer = trace.get_tracer(__name__)
logger = logging.getLogger(__name__)


@router.get("/{user_id}", response_model=PerformanceMetrics)
async def get_performance_metrics(
    user_id: uuid.UUID,
    from_date: Optional[date] = None,
    to_date: Optional[date] = None,
    topics: Optional[List[str]] = Query(None)
) -> PerformanceMetrics:
    """
    Retrieve comprehensive learning effectiveness metrics.
    
    Args:
        user_id: User ID
        from_date: Start date for metrics (optional)
        to_date: End date for metrics (optional)
        topics: List of topics to filter by (optional)
        
    Returns:
        Performance metrics
        
    Raises:
        HTTPException: If user not found or data retrieval fails
    """
    with tracer.start_as_current_span("API:GetPerformanceMetrics") as span:
        span.set_attribute("user.id", str(user_id))
        if from_date:
            span.set_attribute("from_date", str(from_date))
        if to_date:
            span.set_attribute("to_date", str(to_date))
        if topics:
            span.set_attribute("topics", ",".join(topics))
        
        try:
            # In a real implementation, this would:
            # 1. Retrieve user's learning data and session history
            # 2. Calculate performance metrics across topics
            # 3. Generate personalized recommendations
            
            # For now, we'll return mock data
            from app.models.analytics import LearningProgress
            from datetime import datetime, timedelta
            
            # Create mock topic performance data
            topic_data = {
                "python": TopicPerformance(
                    topic="python",
                    proficiency=0.82,
                    items_studied=65,
                    average_accuracy=0.88,
                    average_response_time_ms=1950,
                    retention_rate=0.82,
                    last_studied=datetime.now() - timedelta(days=1)
                ),
                "fastapi": TopicPerformance(
                    topic="fastapi",
                    proficiency=0.75,
                    items_studied=42,
                    average_accuracy=0.80,
                    average_response_time_ms=2300,
                    retention_rate=0.78,
                    last_studied=datetime.now() - timedelta(days=2)
                ),
                "machine learning": TopicPerformance(
                    topic="machine learning",
                    proficiency=0.45,
                    items_studied=28,
                    average_accuracy=0.68,
                    average_response_time_ms=3100,
                    retention_rate=0.62,
                    last_studied=datetime.now() - timedelta(days=5)
                ),
                "semantic kernel": TopicPerformance(
                    topic="semantic kernel",
                    proficiency=0.35,
                    items_studied=12,
                    average_accuracy=0.60,
                    average_response_time_ms=3500,
                    retention_rate=0.55,
                    last_studied=datetime.now() - timedelta(days=7)
                )
            }
            
            # Filter by topics if provided
            if topics:
                topic_data = {k: v for k, v in topic_data.items() if k in topics}
            
            # Create mock daily stats
            today = date.today()
            daily_stats = {}
            for i in range(7):  # Last 7 days
                day_date = today - timedelta(days=i)
                day_str = day_date.isoformat()
                
                # More activity on recent days
                activity_factor = max(0.5, 1.0 - (i * 0.1))
                
                daily_stats[day_str] = DailyStats(
                    date=day_date,
                    total_time_spent_minutes=int(30 * activity_factor),
                    items_studied=int(20 * activity_factor),
                    new_items_learned=int(5 * activity_factor),
                    accuracy_rate=0.75 + (0.05 * activity_factor),  # Improving over time
                    topics_studied=list(topic_data.keys())[:int(3 * activity_factor)],
                    streaks={
                        "daily_practice": 7 - i if i < 7 else 0,
                        "perfect_sessions": 3 - i if i < 3 else 0
                    }
                )
            
            # Create the overall progress
            overall_progress = LearningProgress(
                user_id=user_id,
                global_proficiency=0.68,
                total_time_spent_hours=12.5,
                total_items_learned=150,
                retention_rate=0.75,
                topic_progression={topic: data.proficiency for topic, data in topic_data.items()}
            )
            
            # Create the learning curve data
            learning_curve = {
                topic: [
                    max(0.1, min(1.0, perf.proficiency - 0.2 + (0.05 * i)))
                    for i in range(5)  # 5 data points per topic
                ]
                for topic, perf in topic_data.items()
            }
            
            # Create personalized recommendations
            recommendations = {
                "focus_topics": ["machine learning", "semantic kernel"],
                "review_needed": ["fastapi"] if "fastapi" in topic_data else [],
                "suggested_pace": "medium",
                "next_milestone": "Complete 3 more machine learning modules to reach Competent level"
            }
            
            # Create the full metrics
            metrics = PerformanceMetrics(
                user_id=user_id,
                overall_progress=overall_progress,
                topic_performance=topic_data,
                daily_stats=daily_stats,
                learning_curve=learning_curve,
                recommendations=recommendations
            )
            
            logger.info(f"Retrieved performance metrics for user {user_id}")
            return metrics
            
        except Exception as e:
            error_msg = f"Failed to retrieve performance metrics: {str(e)}"
            logger.error(error_msg)
            span.record_exception(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=error_msg
            )


@router.get("/{user_id}/topic/{topic}", response_model=TopicPerformance)
async def get_topic_performance(user_id: uuid.UUID, topic: str) -> TopicPerformance:
    """
    Retrieve detailed performance metrics for a specific topic.
    
    Args:
        user_id: User ID
        topic: Topic name
        
    Returns:
        Topic-specific performance metrics
        
    Raises:
        HTTPException: If user or topic not found
    """
    with tracer.start_as_current_span("API:GetTopicPerformance") as span:
        span.set_attribute("user.id", str(user_id))
        span.set_attribute("topic", topic)
        
        try:
            # In a real implementation, this would retrieve topic-specific
            # performance data from the analytics service
            
            # For now, we'll return mock data
            from datetime import datetime, timedelta
            
            # Map of topics to mock performance data
            topics = {
                "python": TopicPerformance(
                    topic="python",
                    proficiency=0.82,
                    items_studied=65,
                    average_accuracy=0.88,
                    average_response_time_ms=1950,
                    retention_rate=0.82,
                    last_studied=datetime.now() - timedelta(days=1)
                ),
                "fastapi": TopicPerformance(
                    topic="fastapi",
                    proficiency=0.75,
                    items_studied=42,
                    average_accuracy=0.80,
                    average_response_time_ms=2300,
                    retention_rate=0.78,
                    last_studied=datetime.now() - timedelta(days=2)
                ),
                "machine learning": TopicPerformance(
                    topic="machine learning",
                    proficiency=0.45,
                    items_studied=28,
                    average_accuracy=0.68,
                    average_response_time_ms=3100,
                    retention_rate=0.62,
                    last_studied=datetime.now() - timedelta(days=5)
                ),
                "semantic kernel": TopicPerformance(
                    topic="semantic kernel",
                    proficiency=0.35,
                    items_studied=12,
                    average_accuracy=0.60,
                    average_response_time_ms=3500,
                    retention_rate=0.55,
                    last_studied=datetime.now() - timedelta(days=7)
                )
            }
            
            # Return the topic-specific performance if it exists
            if topic.lower() in topics:
                return topics[topic.lower()]
            else:
                # If the topic doesn't exist, return a 404
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No performance data found for topic: {topic}"
                )
            
        except HTTPException:
            # Re-raise HTTP exceptions
            raise
            
        except Exception as e:
            error_msg = f"Failed to retrieve topic performance: {str(e)}"
            logger.error(error_msg)
            span.record_exception(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=error_msg
            )


@router.get("/{user_id}/daily/{day}", response_model=DailyStats)
async def get_daily_stats(user_id: uuid.UUID, day: date) -> DailyStats:
    """
    Retrieve learning statistics for a specific day.
    
    Args:
        user_id: User ID
        day: The day to retrieve stats for
        
    Returns:
        Daily learning statistics
        
    Raises:
        HTTPException: If user not found or no data for the specified day
    """
    with tracer.start_as_current_span("API:GetDailyStats") as span:
        span.set_attribute("user.id", str(user_id))
        span.set_attribute("day", str(day))
        
        try:
            # In a real implementation, this would retrieve day-specific
            # statistics from the analytics service
            
            # For demonstration, we'll return mock data or a 404 if the day is too old
            today = date.today()
            days_ago = (today - day).days
            
            # Only return data for the last 30 days
            if days_ago < 0 or days_ago > 30:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No stats available for {day}"
                )
            
            # Generate mock stats based on how recent the day is
            activity_factor = max(0.3, 1.0 - (days_ago * 0.03))
            
            stats = DailyStats(
                date=day,
                total_time_spent_minutes=int(30 * activity_factor),
                items_studied=int(20 * activity_factor),
                new_items_learned=int(5 * activity_factor),
                accuracy_rate=0.75 + (0.05 * activity_factor),
                topics_studied=["python", "fastapi"] if days_ago % 2 == 0 else ["machine learning", "semantic kernel"],
                streaks={
                    "daily_practice": min(30, 30 - days_ago) if days_ago <= 30 else 0,
                    "perfect_sessions": min(3, 3 - days_ago) if days_ago <= 3 else 0
                }
            )
            
            logger.info(f"Retrieved daily stats for user {user_id} on {day}")
            return stats
            
        except HTTPException:
            # Re-raise HTTP exceptions
            raise
            
        except Exception as e:
            error_msg = f"Failed to retrieve daily stats: {str(e)}"
            logger.error(error_msg)
            span.record_exception(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=error_msg
            )