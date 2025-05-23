"""
Schedule routes for the AI Learning Assistant API.
"""

import logging
import uuid
from datetime import date, datetime, timedelta
from typing import Dict, Any, List

from fastapi import APIRouter, HTTPException, Depends, status
from opentelemetry import trace

from app.models.scheduling import Schedule, ScheduleRequest
from app.services.spaced_repetition import SpacedRepetitionService
from app.services.question_generator import (
    QuestionGeneratorService, 
    QuestionGenerationRequest, 
    QuestionGenerationResponse,
    Question,
    QuestionType,
    DifficultyLevel,
    QuestionOption
)

# Setup router and tracer
router = APIRouter()
tracer = trace.get_tracer(__name__)
logger = logging.getLogger(__name__)


async def get_spaced_repetition_service() -> SpacedRepetitionService:
    """
    Dependency to get the spaced repetition service.
    
    Returns:
        SpacedRepetitionService instance
    """
    return SpacedRepetitionService()


async def get_question_generator_service() -> QuestionGeneratorService:
    """
    Dependency to get the question generator service.
    
    Returns:
        QuestionGeneratorService instance
    """
    return QuestionGeneratorService()


@router.get("/{user_id}", response_model=Schedule)
async def get_schedule(
    user_id: uuid.UUID,
    from_date: date = None,
    days: int = 7,
    spaced_repetition_service: SpacedRepetitionService = Depends(get_spaced_repetition_service)
) -> Schedule:
    """
    Retrieve a personalized review schedule for a user.
    
    Args:
        user_id: User ID
        from_date: Start date (defaults to today)
        days: Number of days to schedule
        spaced_repetition_service: Service for spaced repetition
        
    Returns:
        Personalized schedule
        
    Raises:
        HTTPException: If user not found or scheduling fails
    """
    with tracer.start_as_current_span("API:GetSchedule") as span:
        span.set_attribute("user.id", str(user_id))
        span.set_attribute("days", days)
        if from_date:
            span.set_attribute("from_date", str(from_date))
        
        try:
            # In a real implementation, this would:
            # 1. Retrieve the user's learning items due for review
            # 2. Use the spaced repetition service to create a schedule
            # 3. Return the personalized schedule
            
            # For now, we'll return mock data
            from app.models.scheduling import DailySchedule
            
            if not from_date:
                from_date = date.today()
            
            # Create a simple mock schedule
            daily_schedules = {}
            for i in range(days):
                # Create a schedule date (today + i days)
                schedule_date = from_date.replace(day=from_date.day + i)
                schedule_date_str = schedule_date.isoformat()
                
                # Create mock items for this day
                items = [uuid.uuid4() for _ in range(3)]
                
                # Create daily schedule
                daily_schedules[schedule_date_str] = DailySchedule(
                    date=schedule_date,
                    user_id=user_id,
                    items=items,
                    total_items=len(items),
                    estimated_time_minutes=len(items) * 3,  # 3 minutes per item
                    new_items_count=1,
                    review_items_count=len(items) - 1
                )
            
            # Create the full schedule
            schedule = Schedule(
                user_id=user_id,
                daily_schedules=daily_schedules,
                total_items_due=sum(s.total_items for s in daily_schedules.values()),
                overdue_items_count=0,
                upcoming_items_count=sum(s.total_items for s in daily_schedules.values())
            )
            
            logger.info(f"Generated schedule for user {user_id} with {schedule.total_items_due} items")
            return schedule
            
        except Exception as e:
            error_msg = f"Failed to retrieve schedule: {str(e)}"
            logger.error(error_msg)
            span.record_exception(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=error_msg
            )


@router.post("/refresh", response_model=Schedule)
async def refresh_schedule(
    request: ScheduleRequest,
    spaced_repetition_service: SpacedRepetitionService = Depends(get_spaced_repetition_service)
) -> Schedule:
    """
    Update schedule based on performance data.
    
    Args:
        request: Schedule request parameters
        spaced_repetition_service: Service for spaced repetition
        
    Returns:
        Updated schedule
        
    Raises:
        HTTPException: If user not found or schedule update fails
    """
    with tracer.start_as_current_span("API:RefreshSchedule") as span:
        span.set_attribute("user.id", str(request.user_id))
        if request.topic_filter:
            span.set_attribute("topic_filter", ",".join(request.topic_filter))
        
        try:
            # In a real implementation, this would:
            # 1. Update the user's learning model based on recent performance
            # 2. Regenerate the schedule with the updated model
            # 3. Return the new personalized schedule
            
            # For now, we'll return a mock schedule similar to get_schedule
            from app.models.scheduling import DailySchedule
            
            days = request.days or 7
            from_date = request.from_date or date.today()
            
            # Create a simple mock schedule
            daily_schedules = {}
            for i in range(days):
                # Create a schedule date (from_date + i days)
                schedule_date = from_date.replace(day=from_date.day + i)
                schedule_date_str = schedule_date.isoformat()
                
                # Create mock items for this day (fewer items on later days)
                item_count = max(1, 5 - (i // 2))
                items = [uuid.uuid4() for _ in range(item_count)]
                
                # Create daily schedule
                daily_schedules[schedule_date_str] = DailySchedule(
                    date=schedule_date,
                    user_id=request.user_id,
                    items=items,
                    total_items=len(items),
                    estimated_time_minutes=len(items) * 3,  # 3 minutes per item
                    new_items_count=1 if i < 3 else 0,  # New items only in first 3 days
                    review_items_count=len(items) - (1 if i < 3 else 0)
                )
            
            # Create the full schedule
            schedule = Schedule(
                user_id=request.user_id,
                daily_schedules=daily_schedules,
                total_items_due=sum(s.total_items for s in daily_schedules.values()),
                overdue_items_count=0,
                upcoming_items_count=sum(s.total_items for s in daily_schedules.values())
            )
            
            logger.info(f"Refreshed schedule for user {request.user_id} with {schedule.total_items_due} items")
            return schedule
            
        except Exception as e:
            error_msg = f"Failed to refresh schedule: {str(e)}"
            logger.error(error_msg)
            span.record_exception(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=error_msg
            )


@router.post("/materials/{material_id}/generate-questions", response_model=QuestionGenerationResponse)
async def generate_questions_for_material(
    material_id: uuid.UUID,
    request: QuestionGenerationRequest,
    question_service: QuestionGeneratorService = Depends(get_question_generator_service)
) -> QuestionGenerationResponse:
    """
    Generate active recall questions for a specific learning material.
    
    Args:
        material_id: ID of the learning material
        request: Question generation parameters
        question_service: Question generator service
        
    Returns:
        Generated questions for active recall practice
        
    Raises:
        HTTPException: If material not found or question generation fails
    """
    with tracer.start_as_current_span("API:GenerateQuestions") as span:
        span.set_attribute("material.id", str(material_id))
        span.set_attribute("question.count", request.question_count)
        
        try:
            # In a real implementation, you would:
            # 1. Fetch the learning material from database
            # 2. Extract content for question generation
            # 3. Use AI service to generate contextual questions
            
            # For now, we'll use mock content
            mock_content = f"""
            This is sample learning material content about programming concepts.
            Variables are used to store data values in programming languages.
            Functions help organize code into reusable blocks.
            Loops allow repetitive execution of code blocks.
            Conditional statements control program flow based on conditions.
            """
            
            # Set the material_id in the request
            request.material_id = material_id
            
            # Generate questions
            response = await question_service.generate_questions_from_material(
                material_content=mock_content,
                request=request
            )
            
            logger.info(f"Generated {response.total_generated} questions for material {material_id}")
            return response
            
        except Exception as e:
            error_msg = f"Failed to generate questions for material {material_id}: {str(e)}"
            logger.error(error_msg)
            span.record_exception(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=error_msg
            )


@router.get("/questions/{question_id}", response_model=Question)
async def get_question(
    question_id: uuid.UUID,
    question_service: QuestionGeneratorService = Depends(get_question_generator_service)
) -> Question:
    """
    Retrieve a specific question by ID.
    
    Args:
        question_id: ID of the question to retrieve
        question_service: Question generator service
        
    Returns:
        The requested question
        
    Raises:
        HTTPException: If question not found
    """
    with tracer.start_as_current_span("API:GetQuestion") as span:
        span.set_attribute("question.id", str(question_id))
        
        try:
            # In a real implementation, this would fetch from database
            # For now, return a mock question
            question = Question(
                id=question_id,
                material_id=uuid.uuid4(),
                question_type=QuestionType.MULTIPLE_CHOICE,
                difficulty=DifficultyLevel.MEDIUM,
                question_text="What is the purpose of variables in programming?",
                correct_answer="A",
                options=[
                    QuestionOption(id="A", text="To store data values", is_correct=True),
                    QuestionOption(id="B", text="To create loops", is_correct=False),
                    QuestionOption(id="C", text="To define functions", is_correct=False),
                    QuestionOption(id="D", text="To handle errors", is_correct=False)
                ],
                explanation="Variables are fundamental constructs used to store and manipulate data in programming.",
                topics=["programming", "variables"]
            )
            
            logger.info(f"Retrieved question {question_id}")
            return question
            
        except Exception as e:
            error_msg = f"Failed to retrieve question {question_id}: {str(e)}"
            logger.error(error_msg)
            span.record_exception(e)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Question {question_id} not found"
            )


@router.put("/questions/{question_id}/response")
async def submit_question_response(
    question_id: uuid.UUID,
    response_data: Dict[str, Any],
    question_service: QuestionGeneratorService = Depends(get_question_generator_service),
    spaced_repetition_service: SpacedRepetitionService = Depends(get_spaced_repetition_service)
) -> Dict[str, Any]:
    """
    Submit a response to a question and get feedback.
    
    Args:
        question_id: ID of the question being answered
        response_data: User's response data including answer and timing
        question_service: Question generator service
        spaced_repetition_service: Spaced repetition service
        
    Returns:
        Feedback and scheduling information
        
    Raises:
        HTTPException: If question not found or response processing fails
    """
    with tracer.start_as_current_span("API:SubmitQuestionResponse") as span:
        span.set_attribute("question.id", str(question_id))
        
        try:
            user_answer = response_data.get("answer", "")
            response_time_ms = response_data.get("response_time_ms", 0)
            
            # Get the question (in real implementation, from database)
            # For now, use a mock question
            question = Question(
                id=question_id,
                material_id=uuid.uuid4(),
                question_type=QuestionType.MULTIPLE_CHOICE,
                difficulty=DifficultyLevel.MEDIUM,
                question_text="What is the purpose of variables in programming?",
                correct_answer="A",
                explanation="Variables are used to store data values in programming.",
                topics=["programming", "variables"]
            )
            
            # Validate the answer
            is_correct, confidence, feedback = await question_service.validate_question_quality(
                question, user_answer
            )
            
            # Calculate next review time using spaced repetition
            # In real implementation, you'd update the learning item
            next_review_date = datetime.now()
            if is_correct:
                # Good response - increase interval
                next_review_date = datetime.now() + timedelta(days=3)
            else:
                # Poor response - review sooner
                next_review_date = datetime.now() + timedelta(days=1)
            
            result = {
                "question_id": str(question_id),
                "is_correct": is_correct,
                "confidence_score": confidence,
                "feedback": feedback,
                "correct_answer": question.correct_answer,
                "explanation": question.explanation,
                "next_review_date": next_review_date.isoformat(),
                "response_time_ms": response_time_ms,
                "performance_data": {
                    "accuracy": 1.0 if is_correct else 0.0,
                    "speed_score": min(1.0, 30000 / max(response_time_ms, 1000)),  # Faster = higher score
                    "difficulty_adjusted_score": confidence * (0.5 + 0.5 * (question.difficulty == DifficultyLevel.HARD))
                }
            }
            
            logger.info(f"Processed response for question {question_id}: correct={is_correct}, confidence={confidence}")
            return result
            
        except Exception as e:
            error_msg = f"Failed to process response for question {question_id}: {str(e)}"
            logger.error(error_msg)
            span.record_exception(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=error_msg
            )


@router.get("/users/{user_id}/active-recall-schedule")
async def get_active_recall_schedule(
    user_id: uuid.UUID,
    include_questions: bool = False,
    spaced_repetition_service: SpacedRepetitionService = Depends(get_spaced_repetition_service),
    question_service: QuestionGeneratorService = Depends(get_question_generator_service)
) -> Dict[str, Any]:
    """
    Get an active recall schedule with questions for a user.
    
    Args:
        user_id: User ID
        include_questions: Whether to include generated questions in the response
        spaced_repetition_service: Spaced repetition service
        question_service: Question generator service
        
    Returns:
        Active recall schedule with optional questions
        
    Raises:
        HTTPException: If user not found or schedule generation fails
    """
    with tracer.start_as_current_span("API:GetActiveRecallSchedule") as span:
        span.set_attribute("user.id", str(user_id))
        span.set_attribute("include_questions", include_questions)
        
        try:
            # Get the regular schedule
            from app.models.scheduling import ScheduleRequest
            
            schedule_request = ScheduleRequest(
                user_id=user_id,
                days=7
            )
            
            # Get basic schedule (simplified call)
            schedule = await get_schedule(user_id, None, 7, spaced_repetition_service)
            
            result = {
                "user_id": str(user_id),
                "schedule": schedule.dict(),
                "active_recall_sessions": [],
                "total_questions_available": 0
            }
            
            if include_questions:
                # Generate sample questions for each day
                for date_str, daily_schedule in schedule.daily_schedules.items():
                    session_questions = []
                    
                    # Generate 2-3 questions per learning item
                    for item_id in daily_schedule.items[:2]:  # Limit to first 2 items for demo
                        request = QuestionGenerationRequest(
                            material_id=item_id,
                            question_count=2,
                            difficulty_level=None
                        )
                        
                        # Mock content for question generation
                        mock_content = "Sample learning content for active recall practice."
                        
                        questions_response = await question_service.generate_questions_from_material(
                            material_content=mock_content,
                            request=request
                        )
                        
                        session_questions.extend([q.dict() for q in questions_response.questions])
                    
                    result["active_recall_sessions"].append({
                        "date": date_str,
                        "item_count": daily_schedule.total_items,
                        "estimated_time_minutes": daily_schedule.estimated_time_minutes,
                        "questions": session_questions
                    })
                    
                    result["total_questions_available"] += len(session_questions)
            
            logger.info(f"Generated active recall schedule for user {user_id}")
            return result
            
        except Exception as e:
            error_msg = f"Failed to generate active recall schedule for user {user_id}: {str(e)}"
            logger.error(error_msg)
            span.record_exception(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=error_msg
            )