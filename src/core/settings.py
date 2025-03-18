from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Настройки конфигурации."""

    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    TEST_DB_HOST: str
    TEST_DB_PORT: int
    TEST_DB_NAME: str
    TEST_POSTGRES_USER: str
    TEST_POSTGRES_PASSWORD: str

    @property
    def async_database_url(self):
        """Асинхронный URL для подключения к PostgreSQL c использованием asyncpg."""
        return (
            f'postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@'
            f'{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'
        )

    @property
    def async_test_database_url(self):
        """Асинхронный URL для подключения к БД для тестов."""
        return (
            f'postgresql+asyncpg://{self.TEST_POSTGRES_USER}:'
            f'{self.TEST_POSTGRES_PASSWORD}@'
            f'{self.TEST_DB_HOST}:{self.TEST_DB_PORT}/{self.TEST_DB_NAME}'
        )

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()  # type: ignore
