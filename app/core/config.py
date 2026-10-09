from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

INSECURE_SECRET_KEYS = {"development_secret_key"}

class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI Setup"
    DATABASE_URL: str = "sqlite:///./sql_app.db"
    SECRET_KEY: str = Field(min_length=32)
    DEBUG_MODE: bool = False
    TOKEN_EXPIRE: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    HASH_ALGORITHM: str = "HS256"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    @field_validator("SECRET_KEY")
    @classmethod
    def validate_secret_key(cls, value: str) -> str:
        if value in INSECURE_SECRET_KEYS:
            raise ValueError("SECRET_KEY must not use a known development value")
        return value

settings = Settings()