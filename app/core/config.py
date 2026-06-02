from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "auth-service"
    ENV: str = "local"

    JWT_SECRET: str
    JWT_ALG: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    SQLITE_PATH: str = "./auth.db"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()