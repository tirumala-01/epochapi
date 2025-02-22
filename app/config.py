from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    REDIS_HOST: str
    DATABASE_URL: str
    ENVIRONMENT: str = "production"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
