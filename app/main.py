from fastapi import FastAPI

from .config import settings
from .routes import auth_routes, chat_routes, user_routes

app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description=settings.description,
    contact=settings.contact,
    license_info=settings.license_info,
)

app.include_router(auth_routes)
app.include_router(chat_routes)
app.include_router(user_routes)
