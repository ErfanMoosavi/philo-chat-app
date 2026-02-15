from contextlib import asynccontextmanager

from fastapi import FastAPI

from .routes import auth_routes, chat_routes, user_routes
from .config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("App startup")
    yield
    print("App shutdown")


app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description=settings.description,
    contact=settings.contact,
    license_info=settings.license_info,
    lifespan=lifespan,
)

app.include_router(auth_routes)
app.include_router(chat_routes)
app.include_router(user_routes)
