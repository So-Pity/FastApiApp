from typing import Literal, Optional
from dotenv import load_dotenv
import os
from pydantic import Field
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)

class Settings(BaseSettings):
    # Application
    APP_DEBUG: bool = Field(
        default=False,
        description="Приложение работает в DEBUG режиме или нет",
    )
    APP_ROOT_PATH: str = Field(
        description="Префикс для всех эндпоинтов API",
        default="/api",
    )
    PROD_MODE: Literal["DEV", "PROD"] = os.getenv(
        "PROD_MODE", "DEV"
    )
    HOST: str = Field(
        default="localhost",
        description="url хоста приложения",
    )

    # Database
    DB_URL: str = Field(
        default="postgresql://admin:admin@localhost:5432/postgres",
        description="Endpoint для базу данных",
    )
    DB_USER: str = Field(
        default="admin",
        description="Имя пользователя для подключения к базе данных",
    )
    DB_PASSWORD: str = Field(
        default="admin",
        description="Пароль пользователя для подключения к базе данных",
    )
    DB_POOL_SIZE: int = Field(
        default=10,
        description="Максимальное количество открытых соединений в открытом пулле к базе данных",
    )

    # Mail
    SUPPORT_EMAIL: str = Field(
        default='support@example.com',
        description='Email support',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.PROD_MODE == "PROD":
            self.CA_FILE_LOCATION = os.getenv("CA_FILE_LOCATION")
            self.CERT_FILE_LOCATION = os.getenv("CERT_FILE_LOCATION")
            self.KEY_FILE_LOCATION = os.getenv("KEY_FILE_LOCATION")
            self.CERT_PASSWORD = os.getenv("CERT_PASSWORD")

class ConstSettings:
    """Constant settings"""

    TITLE: str = "Wallet API"
    LOG_FORMAT: str = "%(asctime)s [%(name)s:%(lineno)s] [%(levelname)s]: %(message)s"

match os.getenv("PROD_MODE", "DEV"):
    case "DEV":
        dotenv_path = "env/.env"
    case "PROD":
        dotenv_path = "env/.env.prod"

settings = Settings(_env_file=dotenv_path)
