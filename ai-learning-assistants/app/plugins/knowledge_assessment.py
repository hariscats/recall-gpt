"""
Knowledge Assessment Plugin for AI Learning Assistant.

This plugin generates practice questions and evaluates responses
to implement active recall learning techniques.
"""

import logging
from typing import Any, Dict, List, Optional, Union
import uuid

from opentelemetry import trace

from app.plugins import LearningPlugin
from app.models.session import Question, QuestionType, ResponseQuality
from app.models.learning_material import LearningItem
from app.services.learning_agent import LearningAgentService


logger = logging.getLogger(__name__)


class QuestionGenerationPlugin(LearningPlugin):
    """Plugin for generating practice questions."""
    
    def __init__(self, learning_agent_service: LearningAgentService):
        """
        Initialize the question generation plugin.
        
        Args:
            learning_agent_service: Service for interacting with the learning agent
        """
        super().__init__("question_generation")
        self.learning_agent_service = learning_agent_service
        
    async def validate(self, **kwargs) -> bool:
        """
        Validate inputs for question generation.
        
        Args:
            **kwargs: Keyword arguments including:
                - learning_item: The learning item to generate questions for
                - question_type: Type of question to generate
                
        Returns:
            Boolean indicating if inputs are valid
        """
        learning_item = kwargs.get("learning_item")
        if not learning_item or not isinstance(learning_item, LearningItem):
            logger.error("Invalid or missing learning item")
            return False
            
        question_type = kwargs.get("question_type")
        if question_type and not isinstance(question_type, QuestionType):
            logger.error("Invalid question type")
            return False
            
        return True
        
    async def run(self, **kwargs) -> Dict[str, Any]:
        """
        Generate practice questions for active recall.
        
        Args:
            **kwargs: Keyword arguments including:
                - learning_item: The learning item to generate questions for
                - question_type: Type of question (defaults to FREE_RESPONSE)
                - difficulty: Difficulty level between 0.0 and 1.0 (defaults to item's difficulty)
                - count: Number of questions to generate (defaults to 1)
                
        Returns:
            Dictionary with generated questions
        """
        with self.tracer.start_as_current_span("Plugin:QuestionGeneration") as span:
            # Validate inputs
            if not await self.validate(**kwargs):
                error_msg = "Invalid inputs for question generation"
                span.set_status(trace.Status(trace.StatusCode.ERROR, error_msg))
                return {"success": False, "error": error_msg}
                
            learning_item = kwargs["learning_item"]
            question_type = kwargs.get("question_type", QuestionType.FREE_RESPONSE)
            difficulty = kwargs.get("difficulty", learning_item.difficulty)
            count = kwargs.get("count", 1)
            
            span.set_attribute("question.type", question_type.value)
            span.set_attribute("question.difficulty", difficulty)
            span.set_attribute("question.count", count)
            span.set_attribute("item.id", str(learning_item.id))
            
            try:
                questions = []
                
                # Generate the requested number of questions
                for _ in range(count):
                    question = await self.learning_agent_service.generate_question(
                        learning_item=learning_item,
                        question_type=question_type,
                        difficulty=difficulty
                    )
                    questions.append(question.dict())
                
                span.add_event(f"Generated {len(questions)} questions")
                
                return {
                    "success": True,
                    "questions": questions,
                    "count": len(questions),
                    "item_id": str(learning_item.id)
                }
                
            except Exception as e:
                error_msg = f"Failed to generate questions: {str(e)}"
                logger.error(error_msg)
                span.record_exception(e)
                
                return {
                    "success": False,
                    "error": error_msg,
                    "item_id": str(learning_item.id)
                }


class AnswerEvaluationPlugin(LearningPlugin):
    """Plugin for evaluating user answers to practice questions."""
    
    def __init__(self, learning_agent_service: LearningAgentService):
        """
        Initialize the answer evaluation plugin.
        
        Args:
            learning_agent_service: Service for interacting with the learning agent
        """
        super().__init__("answer_evaluation")
        self.learning_agent_service = learning_agent_service
        
    async def validate(self, **kwargs) -> bool:
        """
        Validate inputs for answer evaluation.
        
        Args:
            **kwargs: Keyword arguments including:
                - question: The question that was answered
                - user_answer: The user's answer text
                
        Returns:
            Boolean indicating if inputs are valid
        """
        question = kwargs.get("question")
        if not question or not isinstance(question, Question):
            logger.error("Invalid or missing question")
            return False
            
        user_answer = kwargs.get("user_answer")
        if not user_answer or not isinstance(user_answer, str):
            logger.error("Invalid or missing user answer")
            return False
            
        return True
        
    async def run(self, **kwargs) -> Dict[str, Any]:
        """
        Evaluate a user's answer to a question.
        
        Args:
            **kwargs: Keyword arguments including:
                - question: The question that was answered
                - user_answer: The user's answer text
                - response_time_ms: Time taken to answer in milliseconds (optional)
                
        Returns:
            Dictionary with evaluation results
        """
        with self.tracer.start_as_current_span("Plugin:AnswerEvaluation") as span:
            # Validate inputs
            if not await self.validate(**kwargs):
                error_msg = "Invalid inputs for answer evaluation"
                span.set_status(trace.Status(trace.StatusCode.ERROR, error_msg))
                return {"success": False, "error": error_msg}
                
            question = kwargs["question"]
            user_answer = kwargs["user_answer"]
            response_time_ms = kwargs.get("response_time_ms")
            
            span.set_attribute("question.id", str(question.id))
            span.set_attribute("question.type", question.type.value)
            if response_time_ms:
                span.set_attribute("response_time_ms", response_time_ms)
            
            try:
                # Use the learning agent to evaluate the answer
                evaluation = await self.learning_agent_service.evaluate_answer(
                    question=question,
                    user_answer=user_answer
                )
                
                # Determine response quality based on evaluation
                if evaluation.get("is_correct", False):
                    # For correct answers, determine quality based on score or confidence
                    score = evaluation.get("score", 1.0)
                    if score > 0.9:
                        response_quality = ResponseQuality.PERFECT
                    elif score > 0.7:
                        response_quality = ResponseQuality.CORRECT
                    else:
                        response_quality = ResponseQuality.CORRECT_HESITANT
                else:
                    # For incorrect answers
                    if evaluation.get("score", 0.0) > 0.5:
                        response_quality = ResponseQuality.DIFFICULT
                    elif evaluation.get("score", 0.0) > 0.2:
                        response_quality = ResponseQuality.INCORRECT_REMEMBERED
                    else:
                        response_quality = ResponseQuality.INCORRECT
                
                # Add response quality to the evaluation
                evaluation["response_quality"] = int(response_quality)
                evaluation["response_quality_name"] = response_quality.name
                
                span.add_event("Answer evaluated successfully")
                
                return {
                    "success": True,
                    "evaluation": evaluation,
                    "question_id": str(question.id)
                }
                
            except Exception as e:
                error_msg = f"Failed to evaluate answer: {str(e)}"
                logger.error(error_msg)
                span.record_exception(e)
                
                return {
                    "success": False,
                    "error": error_msg,
                    "question_id": str(question.id)
                }


class MasteryAssessmentPlugin(LearningPlugin):
    """Plugin for assessing a user's mastery of topics."""
    
    def __init__(self, learning_agent_service: LearningAgentService):
        """
        Initialize the mastery assessment plugin.
        
        Args:
            learning_agent_service: Service for interacting with the learning agent
        """
        super().__init__("mastery_assessment")
        self.learning_agent_service = learning_agent_service
        
    async def run(self, **kwargs) -> Dict[str, Any]:
        """
        Assess a user's mastery level for a topic.
        
        Args:
            **kwargs: Keyword arguments including:
                - user_id: ID of the user
                - topic: Topic to assess
                - assessment_history: List of past assessment results
                
        Returns:
            Dictionary with mastery assessment
        """
        with self.tracer.start_as_current_span("Plugin:MasteryAssessment") as span:
            user_id = kwargs.get("user_id", "")
            topic = kwargs.get("topic", "")
            assessment_history = kwargs.get("assessment_history", [])
            
            span.set_attribute("user.id", user_id)
            span.set_attribute("topic", topic)
            
            try:
                # This is a simplified implementation that would be more sophisticated
                # in a real application with machine learning models for mastery assessment
                
                # Calculate mastery level from assessment history
                correct_count = sum(1 for a in assessment_history if a.get("is_correct", False))
                total_count = max(1, len(assessment_history))
                accuracy = correct_count / total_count
                
                # Factor in response quality
                avg_quality = 0.0
                if assessment_history:
                    quality_sum = sum(a.get("response_quality", 0) for a in assessment_history)
                    avg_quality = quality_sum / total_count
                
                # Calculate mastery level (simplified algorithm)
                mastery_level = min(1.0, (0.6 * accuracy) + (0.4 * (avg_quality / 5.0)))
                
                # Determine mastery category
                if mastery_level >= 0.9:
                    mastery_category = "Expert"
                elif mastery_level >= 0.75:
                    mastery_category = "Proficient"
                elif mastery_level >= 0.5:
                    mastery_category = "Competent"
                elif mastery_level >= 0.25:
                    mastery_category = "Beginner"
                else:
                    mastery_category = "Novice"
                
                recommendations = []
                if mastery_level < 0.5:
                    recommendations.append("Review fundamental concepts")
                if 0.4 <= mastery_level <= 0.7:
                    recommendations.append("Practice with more challenging questions")
                if mastery_level >= 0.8:
                    recommendations.append("Explore advanced topics")
                
                return {
                    "success": True,
                    "user_id": user_id,
                    "topic": topic,
                    "mastery_level": mastery_level,
                    "mastery_category": mastery_category,
                    "accuracy": accuracy,
                    "assessments_count": total_count,
                    "recommendations": recommendations
                }
                
            except Exception as e:
                error_msg = f"Failed to assess mastery: {str(e)}"
                logger.error(error_msg)
                span.record_exception(e)
                
                return {
                    "success": False,
                    "error": error_msg,
                    "user_id": user_id,
                    "topic": topic
                }