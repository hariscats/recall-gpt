"""
Learning Agent Service for AI Learning Assistant.

This service integrates with Azure OpenAI and Semantic Kernel to provide
intelligent learning capabilities for active recall and content generation.
"""

import logging
import os
from typing import Dict, List, Optional, Any, AsyncIterator

import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from azure.core.credentials import TokenCredential
from opentelemetry import trace

from config import settings
from app.models.learning_material import LearningMaterial, LearningItem
from app.models.session import Question, QuestionType, SessionRequest, RequestResult


# Setup logging
logger = logging.getLogger(__name__)


class LearningAgentService:
    """
    Service for interacting with Azure OpenAI to generate content, questions,
    and provide personalized learning assistance.
    """
    
    def __init__(self):
        """
        Initialize the Learning Agent Service.
        """
        self.tracer = trace.get_tracer(__name__)
        
        # Initialize the Semantic Kernel
        self.kernel = None
        self._initialize_semantic_kernel()
        
    def _initialize_semantic_kernel(self) -> None:
        """
        Initialize the Semantic Kernel with Azure OpenAI.
        
        Raises:
            ValueError: If configuration is invalid or service initialization fails
        """
        with self.tracer.start_as_current_span("LearningAgent:Initialize") as span:
            try:
                # Create a new kernel
                self.kernel = sk.Kernel()
                
                # Configure Azure OpenAI service
                deployment = settings.azure_openai_chat_deployment_name
                endpoint = settings.azure_openai_endpoint
                api_key = settings.azure_openai_api_key
                
                span.set_attribute("azure.deployment", deployment)
                span.set_attribute("azure.endpoint", str(endpoint))
                
                # Add Azure OpenAI service to the kernel
                self.kernel.add_chat_service(
                    "azure_chat_completion",
                    AzureChatCompletion(
                        deployment_name=deployment,
                        endpoint=str(endpoint),
                        api_key=api_key
                    )
                )
                
                logger.info("Semantic Kernel initialized successfully")
                span.add_event("Semantic Kernel initialized")
                
            except Exception as e:
                error_msg = f"Failed to initialize Semantic Kernel: {str(e)}"
                logger.error(error_msg)
                span.record_exception(e)
                span.set_status(trace.Status(trace.StatusCode.ERROR, error_msg))
                raise ValueError(error_msg) from e
    
    async def generate_question(self, 
                          learning_item: LearningItem,
                          question_type: QuestionType = QuestionType.FREE_RESPONSE,
                          difficulty: float = 0.5) -> Question:
        """
        Generate an active recall question from learning content.
        
        Args:
            learning_item: The learning item to generate a question for
            question_type: Type of question to generate
            difficulty: Desired difficulty level (0.0 to 1.0)
            
        Returns:
            Generated question
            
        Raises:
            ValueError: If question generation fails
        """
        with self.tracer.start_as_current_span("LearningAgent:GenerateQuestion") as span:
            span.set_attribute("question_type", question_type.value)
            span.set_attribute("difficulty", difficulty)
            span.set_attribute("item_id", str(learning_item.id))
            
            try:
                # Determine the prompt based on question type
                if question_type == QuestionType.MULTIPLE_CHOICE:
                    system_prompt = """
                    You are an expert educational content creator specializing in multiple-choice questions.
                    Generate a challenging multiple-choice question based on the provided learning content.
                    Make sure the question tests deep understanding rather than simple recall.
                    Provide 4 possible answers, with only one correct answer.
                    Format your response as a JSON object with these fields:
                    {
                        "question": "The question text",
                        "options": ["Option A", "Option B", "Option C", "Option D"],
                        "correct_answer": "The full text of the correct option",
                        "explanation": "Explanation of why this answer is correct"
                    }
                    """
                elif question_type == QuestionType.FILL_IN_BLANK:
                    system_prompt = """
                    You are an expert educational content creator specializing in fill-in-the-blank questions.
                    Generate a fill-in-the-blank question based on the provided learning content.
                    Replace a key concept or term with a blank.
                    Format your response as a JSON object with these fields:
                    {
                        "question": "The question text with _____ for the blank",
                        "correct_answer": "The word or phrase that belongs in the blank",
                        "explanation": "Explanation of why this answer is correct"
                    }
                    """
                else:  # Default to free response
                    system_prompt = """
                    You are an expert educational content creator specializing in open-ended questions.
                    Generate a thought-provoking question based on the provided learning content.
                    The question should encourage deep understanding and application of concepts.
                    Format your response as a JSON object with these fields:
                    {
                        "question": "The question text",
                        "correct_answer": "A model answer to this question",
                        "explanation": "Explanation of important concepts in the answer",
                        "key_points": ["List", "of", "key", "points", "to check for in answers"]
                    }
                    """
                
                # Add difficulty instructions
                if difficulty < 0.3:
                    system_prompt += "\nCreate a basic, straightforward question testing fundamental understanding."
                elif difficulty < 0.7:
                    system_prompt += "\nCreate an intermediate-level question requiring good understanding of the concept."
                else:
                    system_prompt += "\nCreate a challenging question requiring deep understanding and application of the concept."
                
                # Create the user message with content
                user_prompt = f"""
                Learning content: {learning_item.content}
                
                Context: {learning_item.context or ""}
                
                Previous question (avoid repeating): {learning_item.question or "None"}
                """
                
                # Generate the question using Semantic Kernel
                functions = self.kernel.create_semantic_function(
                    system_prompt,
                    temperature=0.7,
                    max_tokens=500,
                    top_p=0.95
                )
                
                result = await self.kernel.invoke_async(functions, input=user_prompt)
                response = result.result
                
                # Parse the response (simplified for brevity - in a real system, add better parsing and error handling)
                import json
                question_data = json.loads(response)
                
                import uuid
                
                # Create a Question object
                question = Question(
                    id=uuid.uuid4(),
                    item_id=learning_item.id,
                    text=question_data["question"],
                    type=question_type,
                    options=question_data.get("options"),
                    correct_answer=question_data["correct_answer"],
                    explanation=question_data["explanation"],
                    metadata={
                        "difficulty": difficulty,
                        "key_points": question_data.get("key_points", [])
                    }
                )
                
                span.add_event("Question generated successfully")
                return question
                
            except Exception as e:
                error_msg = f"Failed to generate question: {str(e)}"
                logger.error(error_msg)
                span.record_exception(e)
                span.set_status(trace.Status(trace.StatusCode.ERROR, error_msg))
                raise ValueError(error_msg) from e
    
    async def evaluate_answer(self, 
                        question: Question, 
                        user_answer: str) -> Dict[str, Any]:
        """
        Evaluate a user's answer to a question.
        
        Args:
            question: The question that was answered
            user_answer: The user's answer text
            
        Returns:
            Dictionary with evaluation results
            
        Raises:
            ValueError: If answer evaluation fails
        """
        with self.tracer.start_as_current_span("LearningAgent:EvaluateAnswer") as span:
            span.set_attribute("question_id", str(question.id))
            span.set_attribute("question_type", question.type.value)
            
            try:
                # Different evaluation approaches based on question type
                if question.type == QuestionType.MULTIPLE_CHOICE:
                    # For multiple choice, do direct comparison
                    is_correct = user_answer.strip().lower() == question.correct_answer.strip().lower()
                    confidence = 1.0  # High confidence in multiple choice evaluation
                    
                    return {
                        "is_correct": is_correct,
                        "confidence": confidence,
                        "explanation": question.explanation,
                        "feedback": "Correct!" if is_correct else f"The correct answer is: {question.correct_answer}"
                    }
                    
                elif question.type == QuestionType.FILL_IN_BLANK:
                    # For fill in blank, check if answer contains the correct term
                    is_correct = question.correct_answer.strip().lower() in user_answer.strip().lower()
                    confidence = 0.9  # High confidence but allowing for slight variations
                    
                    return {
                        "is_correct": is_correct,
                        "confidence": confidence,
                        "explanation": question.explanation,
                        "feedback": "Correct!" if is_correct else f"The correct answer is: {question.correct_answer}"
                    }
                    
                else:  # Free response requires AI evaluation
                    system_prompt = """
                    You are an expert educational evaluator. Assess the user's answer to the given question.
                    Consider the key points that should be included in an ideal answer.
                    Be fair but thorough in your assessment.
                    Format your response as a JSON object with these fields:
                    {
                        "is_correct": true/false (is the answer essentially correct?),
                        "score": 0-1 (how complete is the answer, from 0.0 to 1.0),
                        "feedback": "Constructive feedback on the answer",
                        "missing_points": ["Any", "key", "points", "that", "were", "missing"]
                    }
                    """
                    
                    user_prompt = f"""
                    Question: {question.text}
                    
                    Ideal answer: {question.correct_answer}
                    
                    Key points to check for: {question.metadata.get('key_points', [])}
                    
                    User's answer: {user_answer}
                    """
                    
                    # Use Semantic Kernel to evaluate the answer
                    functions = self.kernel.create_semantic_function(
                        system_prompt,
                        temperature=0.3,  # Lower temperature for more consistent evaluation
                        max_tokens=500
                    )
                    
                    result = await self.kernel.invoke_async(functions, input=user_prompt)
                    response = result.result
                    
                    # Parse the response
                    import json
                    evaluation = json.loads(response)
                    
                    # Add the explanation from the question
                    evaluation["explanation"] = question.explanation
                    
                    return evaluation
                    
            except Exception as e:
                error_msg = f"Failed to evaluate answer: {str(e)}"
                logger.error(error_msg)
                span.record_exception(e)
                span.set_status(trace.Status(trace.StatusCode.ERROR, error_msg))
                raise ValueError(error_msg) from e
    
    async def generate_learning_material(self, 
                                   topic: str, 
                                   difficulty: float = 0.5,
                                   user_preferences: Optional[Dict[str, Any]] = None) -> LearningMaterial:
        """
        Generate new learning material on a specified topic.
        
        Args:
            topic: The topic to generate material about
            difficulty: Desired difficulty level (0.0 to 1.0)
            user_preferences: Optional user preferences to personalize content
            
        Returns:
            Generated learning material
            
        Raises:
            ValueError: If content generation fails
        """
        with self.tracer.start_as_current_span("LearningAgent:GenerateMaterial") as span:
            span.set_attribute("topic", topic)
            span.set_attribute("difficulty", difficulty)
            
            import uuid
            
            try:
                # Personalization hints based on user preferences
                personalization = ""
                if user_preferences:
                    learning_pace = user_preferences.get("learning_pace", "medium")
                    span.set_attribute("user.learning_pace", learning_pace)
                    
                    if learning_pace == "fast":
                        personalization = "Focus on advanced concepts and be concise."
                    elif learning_pace == "slow":
                        personalization = "Explain concepts thoroughly with examples."
                    
                # Create the system prompt
                system_prompt = f"""
                You are an expert educational content creator specializing in creating clear, engaging learning materials.
                Generate comprehensive learning content on the requested topic.
                {personalization}
                
                Format your response as a JSON object with these fields:
                {{
                    "title": "Descriptive title for the material",
                    "description": "Brief overview of what this material covers",
                    "content_blocks": [
                        {{
                            "type": "text",
                            "content": "A paragraph or section of text content",
                            "metadata": {{"format": "markdown"}}
                        }},
                        {{
                            "type": "code",
                            "content": "Code example if applicable",
                            "metadata": {{"language": "appropriate language"}}
                        }}
                        // Include 3-5 content blocks
                    ],
                    "difficulty_level": {difficulty},
                    "topics": ["main topic", "subtopic1", "subtopic2"],
                    "suggested_questions": [
                        "Potential question 1 for active recall",
                        "Potential question 2 for active recall"
                    ]
                }}
                """
                
                # Create the user message
                user_prompt = f"""
                Generate learning material on the topic: {topic}
                
                Difficulty level: {difficulty} (where 0.0 is beginner and 1.0 is expert)
                """
                
                # Generate the material using Semantic Kernel
                functions = self.kernel.create_semantic_function(
                    system_prompt,
                    temperature=0.7,
                    max_tokens=1500,
                    top_p=0.95
                )
                
                result = await self.kernel.invoke_async(functions, input=user_prompt)
                response = result.result
                
                # Parse the response
                import json
                material_data = json.loads(response)
                
                # Create a LearningMaterial object
                from app.models.learning_material import ContentBlock
                
                content_blocks = [
                    ContentBlock(
                        type=block["type"],
                        content=block["content"],
                        metadata=block["metadata"]
                    )
                    for block in material_data["content_blocks"]
                ]
                
                material = LearningMaterial(
                    id=uuid.uuid4(),
                    title=material_data["title"],
                    description=material_data["description"],
                    topics=material_data["topics"],
                    difficulty_level=float(material_data["difficulty_level"]),
                    content_blocks=content_blocks,
                    created_at=datetime.now(),
                    updated_at=datetime.now()
                )
                
                span.add_event("Learning material generated successfully")
                return material
                
            except Exception as e:
                error_msg = f"Failed to generate learning material: {str(e)}"
                logger.error(error_msg)
                span.record_exception(e)
                span.set_status(trace.Status(trace.StatusCode.ERROR, error_msg))
                raise ValueError(error_msg) from e
    
    async def run_learning_session(self, request: SessionRequest) -> RequestResult:
        """
        Start or continue a learning session for a user.
        
        Args:
            request: The session request parameters
            
        Returns:
            Session information with the current question
            
        Raises:
            ValueError: If session creation fails
        """
        with self.tracer.start_as_current_span("LearningAgent:Session") as current_span:
            current_span.set_attribute("user.id", str(request.user_id))
            current_span.set_attribute("session.type", request.session_type.value)
            
            import uuid
            session_id = uuid.uuid4()
            
            try:
                # In a real implementation, this would load existing user sessions
                # and learning materials from a database. For this example, we'll
                # create a placeholder question.
                
                # Create a placeholder question
                example_question = Question(
                    id=uuid.uuid4(),
                    item_id=uuid.uuid4(),  # This would be a real learning item ID in practice
                    text="What is the primary benefit of spaced repetition over massed practice?",
                    type=QuestionType.FREE_RESPONSE,
                    correct_answer="Spaced repetition improves long-term retention by spacing out review sessions, which strengthens neural pathways more effectively than cramming.",
                    explanation="Research shows that distributing practice over time leads to better long-term memory formation than intensive short-term practice (cramming).",
                    metadata={
                        "difficulty": 0.5,
                        "key_points": [
                            "improved retention",
                            "spacing effect",
                            "neural pathway strengthening",
                            "long-term memory"
                        ]
                    }
                )
                
                # Return session result with the question
                result = RequestResult(
                    session_id=session_id,
                    current_question=example_question,
                    session_stats={
                        "total_questions": 10,
                        "current_position": 1,
                        "correct_answers": 0,
                        "estimated_completion_minutes": 15
                    },
                    next_steps="Answer the current question, then proceed to the next one."
                )
                
                current_span.add_event("Session started successfully")
                return result
                
            except Exception as e:
                error_msg = f"Failed to run learning session: {str(e)}"
                logger.error(error_msg)
                current_span.record_exception(e)
                current_span.set_status(trace.Status(trace.StatusCode.ERROR, error_msg))
                raise ValueError(error_msg) from e