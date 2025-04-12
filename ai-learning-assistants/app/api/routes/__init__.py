"""
API routes package for the AI Learning Assistant.
"""

from app.api.routes.user_routes import router as user_router
from app.api.routes.learning_materials_routes import router as learning_materials_router
from app.api.routes.session_routes import router as sessions_router
from app.api.routes.schedule_routes import router as schedule_router
from app.api.routes.analytics_routes import router as analytics_router

__all__ = [
    "user_router",
    "learning_materials_router",
    "sessions_router",
    "schedule_router",
    "analytics_router",
]