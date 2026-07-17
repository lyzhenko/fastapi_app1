from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Setting(BaseSettings):
    """
    Конфигурация приложения для подключения к базе данных.
    
    Загружает переменные окружения из .env файла и предоставляет
    доступ к параметрам подключения к PostgreSQL базе данных.
    
    Attributes:
        DB_HOST: Хост (адрес) сервера базы данных.
        DB_PORT: Порт для подключения к базе данных.
        DB_USER: Имя пользователя для подключения к БД.
        DB_PASS: Пароль пользователя для подключения к БД.
        DB_NAME: Имя базы данных для подключения.
        DATABASE_URL: Вычисляемое поле - полная строка подключения PostgreSQL.
    """
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Setting()
