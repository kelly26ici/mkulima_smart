from __future__ import anotations


from functools import lru_cache
from typing import Literal

from pydantic import Field, SecretStr computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=False, extra="ignore", populate_by_name=True)

    # App
    ENV_TYPE: Literal["development", "production", "testing"] = Field(default="development", validation_alias="FLASK_ENV")
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    HOST: str = "0.0.0.0"
    PORT: int = 5000

    # Database
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    SQLALCHEMY_DATABASE_URL: str = "sqlite:///db.sqlite"

    #LLM
    OPENAI_API_KEY: SecretStr | None = None
    GROQ_API_KEy: SecretStr

    # Tracing
    LANGSMITH_API_KEY: SecretStr | None = None
    LANGSMITH_TRACING_V2: bool = False
    LANGSMITH_PROJECT: str = "mkulima_smart"

    #Africa's Talking
    AFRICASTALKING_USERNAME: str = "sandbox"
    AFRICASTALKING_API_KEY: SecretStr | None = None

    @computed_field
    @property
    def DEBUG(self) -> bool:
        return self.ENV_TYPE == "testing"

    def flask_config(self) -> dict:
        data = {
                k: v.get_secret_value() if isinstance(v, SecretStr) else v
                }
        return data | {"DEBUG": self.DEBUG, "TESTING": self.TESTING}

lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
