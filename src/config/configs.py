from pathlib import Path

from .base import BaseSetting

BASE_DIR = Path(__file__).parent.parent


class DBSettings(BaseSetting):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


class JWTSettings(BaseSetting):
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_ACCESS_TOKEN_EXPIRES: int
    JWT_REFRESH_TOKEN_EXPIRES: int
    ACCESS_TOKEN_COOKIE_KEY: str
    REFRESH_TOKEN_COOKIE_KEY: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


db_settings = DBSettings()
jwt_settings = JWTSettings()

