"""
Learning materials routes for the AI Learning Assistant API.
"""

import logging
import uuid
from typing import List, Dict, Any, Optional

from fastapi import APIRouter, HTTPException, Depends, status, Query
from opentelemetry import trace

from app.models.learning_material import LearningMaterial, LearningMaterialCreate, ContentBlock
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


@router.post("/", response_model=LearningMaterial, status_code=status.HTTP_201_CREATED)
async def create_learning_material(
    material_data: LearningMaterialCreate, 
    learning_agent_service: LearningAgentService = Depends(get_learning_agent_service)
) -> LearningMaterial:
    """
    Create new learning material.
    
    Args:
        material_data: Learning material data
        learning_agent_service: Service for AI operations
        
    Returns:
        Created learning material
    """
    with tracer.start_as_current_span("API:CreateLearningMaterial") as span:
        span.set_attribute("material.title", material_data.title)
        
        try:
            # In a real implementation, this would save to a database
            # For now, we'll create a mock learning material
            new_material = LearningMaterial(
                id=uuid.uuid4(),
                title=material_data.title,
                description=material_data.description,
                topics=material_data.topics,
                difficulty_level=material_data.difficulty_level,
                content_blocks=material_data.content_blocks,
                source_reference=material_data.source_reference
            )
            
            logger.info(f"Created learning material: {new_material.title}")
            return new_material
            
        except Exception as e:
            error_msg = f"Failed to create learning material: {str(e)}"
            logger.error(error_msg)
            span.record_exception(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=error_msg
            )


@router.get("/{material_id}", response_model=LearningMaterial)
async def get_learning_material(material_id: uuid.UUID) -> LearningMaterial:
    """
    Retrieve learning material by ID.
    
    Args:
        material_id: Material ID to retrieve
        
    Returns:
        Learning material
        
    Raises:
        HTTPException: If material not found
    """
    with tracer.start_as_current_span("API:GetLearningMaterial") as span:
        span.set_attribute("material.id", str(material_id))
        
        try:
            # In a real implementation, this would query a database
            # For now, we'll create a mock learning material
            material = LearningMaterial(
                id=material_id,
                title="Introduction to Semantic Kernel",
                description="Learn the basics of Microsoft's Semantic Kernel framework",
                topics=["semantic kernel", "ai", "llm"],
                difficulty_level=0.4,
                content_blocks=[
                    ContentBlock(
                        type="text",
                        content="Semantic Kernel is an open-source SDK that lets you easily combine AI services like OpenAI, Azure OpenAI, and Hugging Face with conventional programming languages like C# and Python.",
                        metadata={"format": "markdown"}
                    ),
                    ContentBlock(
                        type="code",
                        content='import semantic_kernel as sk\n\nkernel = sk.Kernel()\nkernel.add_chat_service("azure", AzureChatCompletion())',
                        metadata={"language": "python"}
                    )
                ]
            )
            
            return material
            
        except Exception as e:
            error_msg = f"Error retrieving learning material: {str(e)}"
            logger.error(error_msg)
            span.record_exception(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=error_msg
            )


@router.post("/generate", response_model=LearningMaterial)
async def generate_learning_material(
    topic: str,
    difficulty: float = 0.5,
    learning_agent_service: LearningAgentService = Depends(get_learning_agent_service)
) -> LearningMaterial:
    """
    Generate learning material on a specified topic using AI.
    
    Args:
        topic: Topic to generate material about
        difficulty: Difficulty level (0.0 to 1.0)
        learning_agent_service: Service for AI operations
        
    Returns:
        Generated learning material
        
    Raises:
        HTTPException: If generation fails
    """
    with tracer.start_as_current_span("API:GenerateLearningMaterial") as span:
        span.set_attribute("topic", topic)
        span.set_attribute("difficulty", difficulty)
        
        try:
            # Use the learning agent service to generate content
            material = await learning_agent_service.generate_learning_material(
                topic=topic,
                difficulty=difficulty
            )
            
            logger.info(f"Generated learning material on topic: {topic}")
            return material
            
        except Exception as e:
            error_msg = f"Failed to generate learning material: {str(e)}"
            logger.error(error_msg)
            span.record_exception(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=error_msg
            )


@router.get("/", response_model=List[LearningMaterial])
async def list_learning_materials(
    topic: Optional[str] = None,
    difficulty_min: Optional[float] = None,
    difficulty_max: Optional[float] = None,
    limit: int = Query(default=10, le=50)
) -> List[LearningMaterial]:
    """
    List learning materials with optional filtering.
    
    Args:
        topic: Filter by topic
        difficulty_min: Minimum difficulty level
        difficulty_max: Maximum difficulty level
        limit: Maximum number of results to return
        
    Returns:
        List of learning materials
    """
    with tracer.start_as_current_span("API:ListLearningMaterials") as span:
        if topic:
            span.set_attribute("filter.topic", topic)
        if difficulty_min is not None:
            span.set_attribute("filter.difficulty_min", difficulty_min)
        if difficulty_max is not None:
            span.set_attribute("filter.difficulty_max", difficulty_max)
        
        try:
            # In a real implementation, this would query a database
            # For now, we'll return a mock list
            materials = [
                LearningMaterial(
                    id=uuid.uuid4(),
                    title="Introduction to Python",
                    description="Learn the basics of Python programming",
                    topics=["python", "programming"],
                    difficulty_level=0.2,
                    content_blocks=[
                        ContentBlock(
                            type="text",
                            content="Python is a high-level, interpreted programming language...",
                            metadata={"format": "markdown"}
                        )
                    ]
                ),
                LearningMaterial(
                    id=uuid.uuid4(),
                    title="Advanced FastAPI Techniques",
                    description="Learn advanced concepts in FastAPI",
                    topics=["python", "fastapi", "advanced"],
                    difficulty_level=0.8,
                    content_blocks=[
                        ContentBlock(
                            type="text",
                            content="FastAPI provides several advanced features...",
                            metadata={"format": "markdown"}
                        )
                    ]
                )
            ]
            
            # Apply filters (if this were a real implementation)
            if topic:
                # This is a simplified filter for demonstration purposes
                materials = [m for m in materials if topic.lower() in [t.lower() for t in m.topics]]
            
            if difficulty_min is not None:
                materials = [m for m in materials if m.difficulty_level >= difficulty_min]
                
            if difficulty_max is not None:
                materials = [m for m in materials if m.difficulty_level <= difficulty_max]
            
            # Limit results
            materials = materials[:limit]
            
            return materials
            
        except Exception as e:
            error_msg = f"Error retrieving learning materials: {str(e)}"
            logger.error(error_msg)
            span.record_exception(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=error_msg
            )