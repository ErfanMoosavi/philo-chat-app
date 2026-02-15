from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # App settings
    app_name: str = "Philo-Chat"
    version: str = "0.1.0"
    description: str = "Chat with your favorite philosophers - Nietzsche, Socrates, and more-in real-time!"
    contact: dict[str, str] = {
        "name": "Erfan Moosavi",
        "email": "erfanmoosavi84@gmail.com",
    }
    license_info: dict[str, str] = {"name": "MIT"}

    # JWT settings
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    # LLM API settings
    base_url: str = "https://api.openai.com/v1"
    api_key: str
    llm_model: str = "google/gemma-3n-e4b-it"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


settings = Settings()
