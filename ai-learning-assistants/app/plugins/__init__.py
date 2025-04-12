"""
Plugin package providing AI-powered functionality for the learning assistant.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from opentelemetry import trace


class LearningPlugin(ABC):
    """Base interface for learning assistant plugins."""
    
    def __init__(self, name: str):
        """
        Initialize the plugin with a name.
        
        Args:
            name: Name of the plugin
        """
        self.name = name
        self.tracer = trace.get_tracer(__name__)
    
    @abstractmethod
    async def run(self, **kwargs) -> Dict[str, Any]:
        """
        Execute the plugin functionality.
        
        Returns:
            Dict containing the plugin execution results
        """
        pass
    
    async def validate(self, **kwargs) -> bool:
        """
        Validate inputs before running the plugin.
        
        Returns:
            Boolean indicating if inputs are valid
        """
        return True


__all__ = ["LearningPlugin"]