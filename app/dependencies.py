import os
from fastapi import Request
from dotenv import load_dotenv
from .services import PhiloChat

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("BASE_URL")
model = os.getenv("MODEL")


def get_philo_chat() -> PhiloChat:
    return PhiloChat(api_key=api_key, base_url=base_url, model_name=model)


def get_username_from_header(request: Request) -> str:
    username = request.headers.get("X-Username")
    return username
