from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    DEEPSEEK_BASE_URL: str = "http://localhost:11434/v1"
    DEEPSEEK_MODEL: str = "deepseek-r1:7b"

    SERVICE_HOST: str = "0.0.0.0"
    SERVICE_PORT: int = 8080

    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings: Settings = Settings()
