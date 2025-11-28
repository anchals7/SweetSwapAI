from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "SweetSwap AI"
    environment: str = Field(default="development")
    database_url: str = Field(
        default="postgresql+psycopg2://sweetswap_user:password@localhost:5432/sweetswap",
        env="DATABASE_URL",
    )
    redis_url: str = Field(default="redis://localhost:6379/0", env="REDIS_URL")
    openai_api_key: str | None = Field(default=None, env="OPENAI_API_KEY")
    gemini_api_key: str | None = Field(default=None, env="GEMINI_API_KEY")
    nutrition_api_key: str | None = Field(default=None, env="NUTRITION_API_KEY")

    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    return Settings()

