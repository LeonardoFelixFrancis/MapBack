from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI Setup"
    DATABASE_URL: str = "sqlite:///./sql_app.db"
    SECRET_KEY: str = "development_secret_key"
    DEBUG_MODE: bool = False
    TOKEN_EXPIRE: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    HASH_ALGORITHM: str = "HS256"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()