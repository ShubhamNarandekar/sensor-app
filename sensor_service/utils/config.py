from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    db_connection: str
    db_name: str
    model_config = SettingsConfigDict(
        env_file=".env",)

# This object can then be used in other files to access the env vars from .env file
settings = Settings()

