from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SECRET_KEY: str

    APP_NAME: str = "@CernunnosYQ's Personal Blog API"
    APP_VERSION: str = "0.1.0"

    CORS_ORIGINS: str
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int

    model_config = SettingsConfigDict(env_file=".env")

    @property
    def DB_URL(self):
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def TEST_DB_URL(self):
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/test_{self.DB_NAME}"


settings = Settings()
