from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    PROJECT_NAME: str = "Hero API"
    DATABASE_URL: str
    DEBUG: bool = False
    ENCRYPTION_KEY: str

    # JWT Settings
    JWT_SECRET: str  # Change in production
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION: int = 30  # minutes
    GOOGLE_API_KEY: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()
