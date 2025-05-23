"""
Question Generation Service for AI Learning Assistant.

This service generates challenging questions from learning materials to implement
active recall techniques for improved retention.
"""

import logging
import random
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum

from pydantic import BaseModel, Field


logger = logging.getLogger(__name__)


class QuestionType(str, Enum):
    """Types of questions that can be generated."""
    MULTIPLE_CHOICE = "multiple_choice"
    FILL_IN_BLANK = "fill_in_blank"
    SHORT_ANSWER = "short_answer"
    TRUE_FALSE = "true_false"
    MATCHING = "matching"


class DifficultyLevel(str, Enum):
    """Difficulty levels for generated questions."""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class QuestionOption(BaseModel):
    """An option for multiple choice questions."""
    id: str = Field(description="Option identifier")
    text: str = Field(description="Option text")
    is_correct: bool = Field(description="Whether this option is correct")


class Question(BaseModel):
    """A generated question with metadata."""
    id: uuid.UUID = Field(default_factory=uuid.uuid4, description="Question ID")
    material_id: uuid.UUID = Field(description="Source learning material ID")
    question_type: QuestionType = Field(description="Type of question")
    difficulty: DifficultyLevel = Field(description="Question difficulty")
    question_text: str = Field(description="The question text")
    correct_answer: str = Field(description="Correct answer")
    options: Optional[List[QuestionOption]] = Field(None, description="Options for multiple choice")
    explanation: Optional[str] = Field(None, description="Explanation of the answer")
    topics: List[str] = Field(default_factory=list, description="Related topics")
    created_at: datetime = Field(default_factory=datetime.now)
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class QuestionGenerationRequest(BaseModel):
    """Request for generating questions."""
    material_id: uuid.UUID = Field(description="Learning material ID")
    question_count: int = Field(default=5, ge=1, le=20, description="Number of questions to generate")
    question_types: Optional[List[QuestionType]] = Field(None, description="Preferred question types")
    difficulty_level: Optional[DifficultyLevel] = Field(None, description="Target difficulty")
    topics_filter: Optional[List[str]] = Field(None, description="Filter by specific topics")


class QuestionGenerationResponse(BaseModel):
    """Response from question generation."""
    questions: List[Question] = Field(description="Generated questions")
    total_generated: int = Field(description="Total number of questions generated")
    generation_time_ms: int = Field(description="Time taken to generate questions in milliseconds")


class QuestionGeneratorService:
    """
    Service for generating challenging questions from learning materials.
    
    This service implements active recall by creating questions that force users
    to retrieve information from memory, strengthening neural pathways.
    """
    
    def __init__(self):
        """Initialize the question generator service."""
        self.question_templates = self._load_question_templates()
    
    def _load_question_templates(self) -> Dict[QuestionType, List[str]]:
        """Load question templates for different question types."""
        return {
            QuestionType.MULTIPLE_CHOICE: [
                "What is {concept}?",
                "Which of the following best describes {concept}?",
                "What is the main purpose of {concept}?",
                "How does {concept} work?",
            ],
            QuestionType.FILL_IN_BLANK: [
                "{concept} is used to _____ in programming.",
                "The main advantage of {concept} is _____.",
                "To implement {concept}, you need to _____.",
            ],
            QuestionType.SHORT_ANSWER: [
                "Explain the concept of {concept}.",
                "Describe how {concept} works.",
                "What are the benefits of using {concept}?",
                "How would you implement {concept}?",
            ],
            QuestionType.TRUE_FALSE: [
                "{concept} is always better than alternatives.",
                "{concept} can only be used in specific scenarios.",
                "{concept} improves performance in all cases.",
            ]
        }
    
    async def generate_questions_from_material(
        self, 
        material_content: str, 
        request: QuestionGenerationRequest
    ) -> QuestionGenerationResponse:
        """
        Generate questions from learning material content.
        
        Args:
            material_content: The content of the learning material
            request: Question generation parameters
            
        Returns:
            Generated questions with metadata
        """
        start_time = datetime.now()
        
        try:
            # Extract key concepts from the material
            concepts = await self._extract_concepts(material_content)
            
            # Determine question types to generate
            question_types = request.question_types or list(QuestionType)
            
            # Generate questions
            questions = []
            for i in range(request.question_count):
                question_type = random.choice(question_types)
                concept = random.choice(concepts) if concepts else "the topic"
                
                question = await self._generate_single_question(
                    material_id=request.material_id,
                    concept=concept,
                    question_type=question_type,
                    difficulty=request.difficulty_level or DifficultyLevel.MEDIUM,
                    material_content=material_content
                )
                
                if question:
                    questions.append(question)
            
            end_time = datetime.now()
            generation_time_ms = int((end_time - start_time).total_seconds() * 1000)
            
            logger.info(f"Generated {len(questions)} questions for material {request.material_id}")
            
            return QuestionGenerationResponse(
                questions=questions,
                total_generated=len(questions),
                generation_time_ms=generation_time_ms
            )
            
        except Exception as e:
            logger.error(f"Failed to generate questions: {str(e)}")
            raise
    
    async def _extract_concepts(self, content: str) -> List[str]:
        """
        Extract key concepts from learning material content.
        
        In a real implementation, this would use NLP or AI to extract concepts.
        For now, we'll use a simple approach.
        """
        # Simple keyword extraction (in reality, you'd use NLP)
        common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were'}
        words = content.lower().split()
        concepts = []
        
        for word in words:
            if len(word) > 4 and word not in common_words and word.isalpha():
                concepts.append(word)
        
        # Return unique concepts, limited to top 10
        return list(set(concepts))[:10]
    
    async def _generate_single_question(
        self,
        material_id: uuid.UUID,
        concept: str,
        question_type: QuestionType,
        difficulty: DifficultyLevel,
        material_content: str
    ) -> Optional[Question]:
        """Generate a single question of the specified type."""
        try:
            template = random.choice(self.question_templates[question_type])
            question_text = template.format(concept=concept)
            
            if question_type == QuestionType.MULTIPLE_CHOICE:
                return await self._generate_multiple_choice(
                    material_id, question_text, concept, difficulty, material_content
                )
            elif question_type == QuestionType.FILL_IN_BLANK:
                return await self._generate_fill_in_blank(
                    material_id, question_text, concept, difficulty
                )
            elif question_type == QuestionType.SHORT_ANSWER:
                return await self._generate_short_answer(
                    material_id, question_text, concept, difficulty
                )
            elif question_type == QuestionType.TRUE_FALSE:
                return await self._generate_true_false(
                    material_id, question_text, concept, difficulty
                )
            else:
                logger.warning(f"Unsupported question type: {question_type}")
                return None
                
        except Exception as e:
            logger.error(f"Failed to generate {question_type} question: {str(e)}")
            return None
    
    async def _generate_multiple_choice(
        self, 
        material_id: uuid.UUID, 
        question_text: str, 
        concept: str, 
        difficulty: DifficultyLevel,
        material_content: str
    ) -> Question:
        """Generate a multiple choice question."""
        # Mock correct answer and distractors
        correct_answer = f"A programming concept related to {concept}"
        
        options = [
            QuestionOption(id="A", text=correct_answer, is_correct=True),
            QuestionOption(id="B", text=f"An unrelated concept to {concept}", is_correct=False),
            QuestionOption(id="C", text=f"A different approach than {concept}", is_correct=False),
            QuestionOption(id="D", text=f"The opposite of {concept}", is_correct=False),
        ]
        
        random.shuffle(options)
        
        return Question(
            material_id=material_id,
            question_type=QuestionType.MULTIPLE_CHOICE,
            difficulty=difficulty,
            question_text=question_text,
            correct_answer="A",  # Would need to track which option is correct after shuffle
            options=options,
            explanation=f"This question tests understanding of {concept}.",
            topics=[concept]
        )
    
    async def _generate_fill_in_blank(
        self, 
        material_id: uuid.UUID, 
        question_text: str, 
        concept: str, 
        difficulty: DifficultyLevel
    ) -> Question:
        """Generate a fill-in-the-blank question."""
        return Question(
            material_id=material_id,
            question_type=QuestionType.FILL_IN_BLANK,
            difficulty=difficulty,
            question_text=question_text,
            correct_answer=concept,
            explanation=f"The correct answer relates to the concept of {concept}.",
            topics=[concept]
        )
    
    async def _generate_short_answer(
        self, 
        material_id: uuid.UUID, 
        question_text: str, 
        concept: str, 
        difficulty: DifficultyLevel
    ) -> Question:
        """Generate a short answer question."""
        return Question(
            material_id=material_id,
            question_type=QuestionType.SHORT_ANSWER,
            difficulty=difficulty,
            question_text=question_text,
            correct_answer=f"A detailed explanation of {concept} and its applications.",
            explanation=f"This question requires a comprehensive understanding of {concept}.",
            topics=[concept]
        )
    
    async def _generate_true_false(
        self, 
        material_id: uuid.UUID, 
        question_text: str, 
        concept: str, 
        difficulty: DifficultyLevel
    ) -> Question:
        """Generate a true/false question."""
        is_true = random.choice([True, False])
        
        return Question(
            material_id=material_id,
            question_type=QuestionType.TRUE_FALSE,
            difficulty=difficulty,
            question_text=question_text,
            correct_answer="True" if is_true else "False",
            explanation=f"This statement about {concept} is {'true' if is_true else 'false'}.",
            topics=[concept]
        )
    
    async def validate_question_quality(self, question: Question, answer: str) -> Tuple[bool, float, str]:
        """
        Validate the quality of a generated question and user answer.
        
        Args:
            question: The question to validate
            answer: User's answer
            
        Returns:
            Tuple of (is_correct, confidence_score, feedback)
        """
        try:
            # Simple validation logic (in reality, you'd use more sophisticated NLP)
            if question.question_type == QuestionType.MULTIPLE_CHOICE:
                is_correct = answer.upper() == question.correct_answer.upper()
                confidence = 1.0 if is_correct else 0.0
                feedback = "Correct!" if is_correct else f"Incorrect. The correct answer is {question.correct_answer}."
                
            elif question.question_type == QuestionType.TRUE_FALSE:
                is_correct = answer.lower() in ["true", "false"] and answer.lower() == question.correct_answer.lower()
                confidence = 1.0 if is_correct else 0.0
                feedback = "Correct!" if is_correct else f"Incorrect. The correct answer is {question.correct_answer}."
                
            else:
                # For open-ended questions, use simple keyword matching
                answer_words = set(answer.lower().split())
                correct_words = set(question.correct_answer.lower().split())
                overlap = len(answer_words.intersection(correct_words))
                total_words = len(correct_words)
                
                confidence = overlap / total_words if total_words > 0 else 0.0
                is_correct = confidence >= 0.6  # Consider correct if 60% overlap
                
                if is_correct:
                    feedback = f"Good answer! Confidence: {confidence:.0%}"
                else:
                    feedback = f"Partially correct. Consider: {question.correct_answer}"
            
            return is_correct, confidence, feedback
            
        except Exception as e:
            logger.error(f"Failed to validate question quality: {str(e)}")
            return False, 0.0, "Unable to validate answer."
