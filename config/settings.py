import os
from pydantic import Field
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    ETH_WSS_URL: str = Field(default=os.getenv("ETH_WSS_URL", ""))
    ETH_HTTP_URL: str = Field(default=os.getenv("ETH_HTTP_URL", ""))
    PRIVATE_KEY: str = Field(default=os.getenv("PRIVATE_KEY", ""))
    PUBLIC_ADDRESS: str = Field(default=os.getenv("PUBLIC_ADDRESS", ""))
    DATABASE_URL: str = Field(default=os.getenv("DATABASE_URL", "sqlite:///mev_bot.db"))
    OLLAMA_HOST: str = Field(default=os.getenv("OLLAMA_HOST", "http://localhost:11434"))

    class Config:
        case_sensitive = True

settings = Settings()
