from contextlib import asynccontextmanager

from fastapi import FastAPI
from routes import auth_routes, chat_routes, user_routes


@asynccontextmanager
def lifespan():
    print("App startup")
    yield
    print("App shutdown")


app = FastAPI(
    title="Philo-Chat",
    version="0.1.0",
    description="Chat with your favorite philosophers - Nietzsche, Socrates, and more-in real-time!",
    contact={"name": "Erfan Moosavi", "email": "erfanmoosavi84@gmail.com"},
    license_info={"name": "MIT"},
    lifespan=lifespan,
)

app.include_router(auth_routes)
app.include_router(chat_routes)
app.include_router(user_routes)
