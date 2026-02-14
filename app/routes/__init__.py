from .auth import router as auth_routes
from .chat import router as chat_routes
from .user import router as user_routes

__all__ = ["auth_routes", "chat_routes", "user_routes"]
