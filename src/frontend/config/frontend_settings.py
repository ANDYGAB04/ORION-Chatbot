from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    CHAT_ENDPOINT_URL: str = "http://localhost:8000/chat/answer"

    class Config:
        env_file = ".env"
        extra = "allow"
