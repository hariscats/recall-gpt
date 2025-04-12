"""
Learning session routes for the AI Learning Assistant API.
"""

import logging
import uuid
from typing import Dict, Any

from fastapi import APIRouter, HTTPException, Depends, status
from opentelemetry import trace

from app.models.session import (
    SessionRequest, 
    RequestResult, 
    Question,
    UserAnswer,
    LearningFeedback,
    Session
)
from app.services.learning_agent import LearningAgentService

# Setup router and tracer
router = APIRouter()
tracer = trace.get_tracer(__name__)
logger = logging.getLogger(__name__)


async def get_learning_agent_service() -> LearningAgentService:
    """
    Dependency to get the learning agent service.
    
    Returns:
        LearningAgentService instance
    """
    return LearningAgentService()


@router.post("/start", response_model=RequestResult)
async def start_session(
    request: SessionRequest,
    learning_agent_service: LearningAgentService = Depends(get_learning_agent_service)
) -> RequestResult:
    """
    Initiate a new learning session.
    
    Args:
        request: Session request parameters
        learning_agent_service: Service for AI operations
        
    Returns:
        Session result with first question
    """
    with tracer.start_as_current_span("API:StartSession") as span:
        span.set_attribute("user.id", str(request.user_id))
        span.set_attribute("session.type", request.session_type.value)
        
        try:
            # Use the learning agent service to create a session
            session_result = await learning_agent_service.run_learning_session(request)
            
            logger.info(f"Started session for user: {request.user_id}")
            return session_result
            
        except Exception as e:
            error_msg = f"Failed to start learning session: {str(e)}"
            logger.error(error_msg)
            span.record_exception(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=error_msg
            )


@router.post("/{session_id}/practice", response_model=Question)
async def generate_practice_question(
    session_id: uuid.UUID,
    learning_agent_service: LearningAgentService = Depends(get_learning_agent_service)
) -> Question:
    """
    Generate a practice question for the current session.
    
    Args:
        session_id: Session ID
        learning_agent_service: Service for AI operations
        
    Returns:
        Generated question
        
    Raises:
        HTTPException: If session not found or question generation fails
    """
    with tracer.start_as_current_span("API:GeneratePracticeQuestion") as span:
        span.set_attribute("session.id", str(session_id))
        
        try:
            # In a real implementation, this would retrieve session data
            # and generate a question based on the user's learning progress
            # For now, we'll return a mock question
            
            question = Question(
                id=uuid.uuid4(),
                item_id=uuid.uuid4(),
                text="What are the primary benefits of active recall in learning?",
                type="free_response",
                correct_answer="Active recall strengthens memory by forcing the brain to retrieve information, which builds stronger neural pathways than passive review.",
                explanation="Active recall is more effective than passive review because it simulates real-world use of knowledge and strengthens memory retrieval pathways.",
                metadata={
                    "difficulty": 0.6,
                    "key_points": [
                        "strengthens memory",
                        "builds neural pathways",
                        "more effective than passive review",
                        "simulates real usage"
                    ]
                }
            )
            
            logger.info(f"Generated practice question for session: {session_id}")
            return question
            
        except Exception as e:
            error_msg = f"Failed to generate practice question: {str(e)}"
            logger.error(error_msg)
            span.record_exception(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=error_msg
            )


@router.post("/{session_id}/feedback", response_model=LearningFeedback)
async def submit_answer(
    session_id: uuid.UUID,
    user_answer: UserAnswer,
    learning_agent_service: LearningAgentService = Depends(get_learning_agent_service)
) -> LearningFeedback:
    """
    Submit a user's answer and get feedback.
    
    Args:
        session_id: Session ID
        user_answer: User's answer data
        learning_agent_service: Service for AI operations
        
    Returns:
        Feedback on the answer
        
    Raises:
        HTTPException: If session not found or evaluation fails
    """
    with tracer.start_as_current_span("API:SubmitAnswer") as span:
        span.set_attribute("session.id", str(session_id))
        span.set_attribute("question.id", str(user_answer.question_id))
        span.set_attribute("response_time_ms", user_answer.response_time_ms)
        
        try:
            # In a real implementation, this would:
            # 1. Retrieve the question from the session
            # 2. Evaluate the answer using the learning agent
            # 3. Update the user's learning model based on performance
            # 4. Return personalized feedback
            
            # For now, we'll return mock feedback
            feedback = LearningFeedback(
                question_id=user_answer.question_id,
                is_correct=True,
                quality=user_answer.self_evaluation or 4,  # Default to CORRECT if not provided
                explanation="Active recall strengthens memory by forcing retrieval, which builds stronger neural pathways than passive review.",
                next_steps="Try applying this concept by creating your own practice questions on other topics you're learning.",
                updated_difficulty=0.65,  # Slightly increased difficulty
                next_review_interval=4.0  # 4 days until next review
            )
            
            logger.info(f"Processed answer for session: {session_id}")
            return feedback
            
        except Exception as e:
            error_msg = f"Failed to process answer: {str(e)}"
            logger.error(error_msg)
            span.record_exception(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=error_msg
            )


@router.get("/{session_id}", response_model=Session)
async def get_session(session_id: uuid.UUID) -> Session:
    """
    Retrieve information about a learning session.
    
    Args:
        session_id: Session ID
        
    Returns:
        Session information
        
    Raises:
        HTTPException: If session not found
    """
    with tracer.start_as_current_span("API:GetSession") as span:
        span.set_attribute("session.id", str(session_id))
        
        try:
            # In a real implementation, this would retrieve session data from storage
            # For now, we'll return mock data
            from datetime import datetime
            
            session = Session(
                id=session_id,
                user_id=uuid.uuid4(),
                type="mixed",
                status="active",
                started_at=datetime.now(),
                items=[uuid.uuid4(), uuid.uuid4()],
                current_item_index=0
            )
            
            return session
            
        except Exception as e:
            error_msg = f"Failed to retrieve session: {str(e)}"
            logger.error(error_msg)
            span.record_exception(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=error_msg
            )