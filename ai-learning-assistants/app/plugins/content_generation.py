"""
Content Generation Plugin for AI Learning Assistant.

This plugin generates learning content using Azure OpenAI and Semantic Kernel.
"""

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional, Union
import uuid

from opentelemetry import trace

from app.plugins import LearningPlugin
from app.models.learning_material import LearningMaterial, ContentBlock
from app.services.learning_agent import LearningAgentService


logger = logging.getLogger(__name__)


class ContentGenerationPlugin(LearningPlugin):
    """Plugin for generating learning content."""
    
    def __init__(self, learning_agent_service: LearningAgentService):
        """
        Initialize the content generation plugin.
        
        Args:
            learning_agent_service: Service for interacting with the learning agent
        """
        super().__init__("content_generation")
        self.learning_agent_service = learning_agent_service
        
    async def validate(self, **kwargs) -> bool:
        """
        Validate the inputs for content generation.
        
        Args:
            **kwargs: Keyword arguments including:
                - topic: The topic to generate content for (required)
                - difficulty: Difficulty level between 0.0 and 1.0 (optional)
                - user_preferences: User preferences for personalization (optional)
                
        Returns:
            Boolean indicating if inputs are valid
        """
        # Check if topic is provided and not empty
        topic = kwargs.get("topic")
        if not topic or not isinstance(topic, str) or len(topic.strip()) == 0:
            logger.error("Invalid or missing topic for content generation")
            return False
            
        # Check if difficulty is valid (if provided)
        difficulty = kwargs.get("difficulty")
        if difficulty is not None and (not isinstance(difficulty, (int, float)) or 
                                      difficulty < 0.0 or difficulty > 1.0):
            logger.error("Invalid difficulty level, must be between 0.0 and 1.0")
            return False
            
        # Check if user preferences is a dictionary (if provided)
        user_preferences = kwargs.get("user_preferences")
        if user_preferences is not None and not isinstance(user_preferences, dict):
            logger.error("User preferences must be a dictionary")
            return False
            
        return True
        
    async def run(self, **kwargs) -> Dict[str, Any]:
        """
        Generate learning content for a given topic.
        
        Args:
            **kwargs: Keyword arguments including:
                - topic: The topic to generate content for
                - difficulty: Difficulty level between 0.0 and 1.0 (defaults to 0.5)
                - user_preferences: User preferences for personalization
                - format: Output format (e.g., "markdown", "html")
                
        Returns:
            Dictionary with generated learning material
            
        Raises:
            ValueError: If inputs are invalid or content generation fails
        """
        with self.tracer.start_as_current_span("Plugin:ContentGeneration") as span:
            # Validate inputs
            if not await self.validate(**kwargs):
                error_msg = "Invalid inputs for content generation"
                span.set_status(trace.Status(trace.StatusCode.ERROR, error_msg))
                raise ValueError(error_msg)
                
            topic = kwargs["topic"]
            difficulty = kwargs.get("difficulty", 0.5)
            user_preferences = kwargs.get("user_preferences")
            output_format = kwargs.get("format", "markdown")
            
            span.set_attribute("content.topic", topic)
            span.set_attribute("content.difficulty", difficulty)
            span.set_attribute("content.format", output_format)
            
            try:
                # Generate learning material using the learning agent service
                material = await self.learning_agent_service.generate_learning_material(
                    topic=topic,
                    difficulty=difficulty,
                    user_preferences=user_preferences
                )
                
                # Apply any additional formatting based on the requested output format
                if output_format == "html" and material.content_blocks:
                    for block in material.content_blocks:
                        if block.type == "text" and block.metadata.get("format") == "markdown":
                            # In a real implementation, we would convert markdown to HTML here
                            block.metadata["format"] = "html"
                
                span.add_event("Content generated successfully")
                
                # Return the generated material
                return {
                    "success": True,
                    "material": material.dict(),
                    "topic": topic,
                    "difficulty": difficulty
                }
                
            except Exception as e:
                error_msg = f"Failed to generate content: {str(e)}"
                logger.error(error_msg)
                span.record_exception(e)
                span.set_status(trace.Status(trace.StatusCode.ERROR, error_msg))
                
                return {
                    "success": False,
                    "error": error_msg,
                    "topic": topic
                }


class QuickNoteGenerationPlugin(LearningPlugin):
    """Plugin for generating quick learning notes."""
    
    def __init__(self, learning_agent_service: LearningAgentService):
        """
        Initialize the quick note generation plugin.
        
        Args:
            learning_agent_service: Service for interacting with the learning agent
        """
        super().__init__("quick_note_generation")
        self.learning_agent_service = learning_agent_service
        
    async def run(self, **kwargs) -> Dict[str, Any]:
        """
        Generate a quick learning note on a topic.
        
        Args:
            **kwargs: Keyword arguments including:
                - topic: The topic to generate a note for
                - max_length: Maximum length in words
                
        Returns:
            Dictionary with generated quick note
        """
        with self.tracer.start_as_current_span("Plugin:QuickNoteGeneration") as span:
            topic = kwargs.get("topic", "")
            max_length = kwargs.get("max_length", 200)
            
            span.set_attribute("note.topic", topic)
            span.set_attribute("note.max_length", max_length)
            
            try:
                # Example implementation (in a real app, this would use the learning agent)
                note = LearningMaterial(
                    id=uuid.uuid4(),
                    title=f"Quick Note: {topic}",
                    description=f"A brief summary of key concepts in {topic}",
                    topics=[topic],
                    difficulty_level=0.3,
                    content_blocks=[
                        ContentBlock(
                            type="text",
                            content=f"This is a placeholder for a quick note about {topic}. "
                                   f"In a real implementation, this would be generated by the AI.",
                            metadata={"format": "markdown"}
                        )
                    ],
                    created_at=datetime.now(),
                    updated_at=datetime.now()
                )
                
                return {
                    "success": True,
                    "note": note.dict(),
                    "topic": topic
                }
                
            except Exception as e:
                error_msg = f"Failed to generate quick note: {str(e)}"
                logger.error(error_msg)
                span.record_exception(e)
                
                return {
                    "success": False,
                    "error": error_msg,
                    "topic": topic
                }