"""
Spaced repetition service implementing the SM-2 algorithm with modifications.

This module provides the core functionality for scheduling learning items
based on spaced repetition principles to optimize retention.
"""

import math
import random
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple

from app.models.session import ResponseQuality
from app.models.scheduling import ScheduleItem
from app.models.learning_material import LearningItem


class SpacedRepetitionService:
    """
    Service that implements the SM-2 spaced repetition algorithm.
    
    The algorithm calculates optimal intervals between repetitions based on
    the quality of responses, with adjustments for difficulty and other factors.
    """
    
    # Default parameters for the SM-2 algorithm
    DEFAULT_EASE_FACTOR = 2.5
    MIN_EASE_FACTOR = 1.3
    EASE_FACTOR_MODIFIER = 0.15
    FIRST_INTERVAL = 1.0  # First interval in days
    SECOND_INTERVAL = 6.0  # Second interval in days
    
    def __init__(self, 
                 initial_ease_factor: float = DEFAULT_EASE_FACTOR,
                 min_ease_factor: float = MIN_EASE_FACTOR,
                 ease_factor_modifier: float = EASE_FACTOR_MODIFIER):
        """
        Initialize the spaced repetition service with configurable parameters.
        
        Args:
            initial_ease_factor: Starting ease factor for new items
            min_ease_factor: Minimum value for the ease factor
            ease_factor_modifier: How much the ease factor changes based on response quality
        """
        self.initial_ease_factor = initial_ease_factor
        self.min_ease_factor = min_ease_factor
        self.ease_factor_modifier = ease_factor_modifier
        
    async def calculate_next_review(self, 
                               item: LearningItem, 
                               response_quality: ResponseQuality) -> Tuple[datetime, float, float]:
        """
        Calculate the next review time for a learning item based on response quality.
        
        Args:
            item: The learning item being reviewed
            response_quality: Quality of the user's response
            
        Returns:
            Tuple containing:
                - next_review: DateTime when the item should next be reviewed
                - new_ease_factor: Updated ease factor
                - new_interval_days: New interval in days
        """
        # Only adjust schedule for items with a quality rating of 2 or higher
        if response_quality < ResponseQuality.DIFFICULT:
            # If response was poor, schedule for review soon (within a day)
            hours_delay = 1 if response_quality == ResponseQuality.INCORRECT_REMEMBERED else 0.5
            next_review = datetime.now() + timedelta(hours=hours_delay)
            return next_review, item.ease_factor, hours_delay / 24.0
        
        # Calculate new ease factor based on response quality
        # Formula: EF' = EF + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))
        ease_delta = 0.1 - (5 - int(response_quality)) * (0.08 + (5 - int(response_quality)) * 0.02)
        new_ease_factor = max(self.min_ease_factor, item.ease_factor + ease_delta)
        
        # Calculate new interval
        if item.review_count == 0:
            # First review
            new_interval_days = self.FIRST_INTERVAL
        elif item.review_count == 1:
            # Second review
            new_interval_days = self.SECOND_INTERVAL
        else:
            # Subsequent reviews: I(n) = I(n-1) * EF
            new_interval_days = item.interval_days * new_ease_factor
            
        # Add some variability to avoid clustering of reviews
        variability_factor = 0.95 + (0.1 * random.random())
        new_interval_days *= variability_factor
            
        # Calculate next review date
        next_review = datetime.now() + timedelta(days=new_interval_days)
        
        return next_review, new_ease_factor, new_interval_days
    
    async def schedule_items(self, 
                        items: List[LearningItem], 
                        user_id: str, 
                        max_items_per_day: int = 20) -> Dict[str, List[ScheduleItem]]:
        """
        Schedule a list of learning items for review.
        
        Args:
            items: List of learning items to schedule
            user_id: ID of the user
            max_items_per_day: Maximum number of items to schedule per day
            
        Returns:
            Dictionary mapping date strings (YYYY-MM-DD) to lists of scheduled items
        """
        # Group items by due date
        schedule_dict: Dict[str, List[ScheduleItem]] = {}
        
        # Sort items by due date and priority
        sorted_items = sorted(items, key=lambda x: (x.next_review, -x.difficulty))
        
        for item in sorted_items:
            due_date = item.next_review.date().isoformat()
            
            # Initialize the day's schedule if it doesn't exist
            if due_date not in schedule_dict:
                schedule_dict[due_date] = []
                
            # Check if we've hit the daily limit
            if len(schedule_dict[due_date]) >= max_items_per_day:
                # Find the next least-loaded day
                while len(schedule_dict.get(due_date, [])) >= max_items_per_day:
                    due_date = (datetime.fromisoformat(due_date) + timedelta(days=1)).date().isoformat()
                    if due_date not in schedule_dict:
                        schedule_dict[due_date] = []
            
            # Calculate priority based on item difficulty and days overdue
            days_overdue = max(0, (datetime.now() - item.next_review).days)
            priority = 0.5 * item.difficulty + 0.5 * min(1.0, days_overdue / 7)
            
            # Estimate review time based on item difficulty and past performance
            estimated_time = 30 + int(item.difficulty * 60)  # between 30s and 90s
            
            # Create schedule item
            schedule_item = ScheduleItem(
                item_id=item.id,
                user_id=user_id,
                due_date=item.next_review,
                priority=priority,
                estimated_time_seconds=estimated_time
            )
            
            # Add to schedule
            schedule_dict[due_date].append(schedule_item)
            
        return schedule_dict
    
    async def update_item_after_review(self,
                                  item: LearningItem,
                                  response_quality: ResponseQuality) -> LearningItem:
        """
        Update a learning item after it has been reviewed.
        
        Args:
            item: The learning item that was reviewed
            response_quality: Quality of the user's response
            
        Returns:
            Updated learning item
        """
        # Calculate next review, ease factor, and interval
        next_review, new_ease_factor, new_interval_days = await self.calculate_next_review(
            item, response_quality
        )
        
        # Update the item
        item.last_reviewed = datetime.now()
        item.next_review = next_review
        item.ease_factor = new_ease_factor
        item.interval_days = new_interval_days
        item.review_count += 1
        
        # Adjust difficulty based on response quality
        if response_quality >= ResponseQuality.CORRECT:
            # Gradually decrease difficulty as the user gets better
            item.difficulty = max(0.1, item.difficulty - 0.05)
        elif response_quality <= ResponseQuality.INCORRECT_REMEMBERED:
            # Increase difficulty for items the user struggles with
            item.difficulty = min(1.0, item.difficulty + 0.1)
        
        return item