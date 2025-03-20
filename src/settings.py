from enum import Enum

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ApplicationMode(Enum):
    DEVELOPMENT = "dev"
    PRODUCTION = "prod"


class AppSettings(BaseSettings):
    MISTRAL_API_KEY: str = Field(default="api-key")
    MISTRAL_MODEL: str = Field(default="codestral-latest")

    MODE: ApplicationMode = Field(default=ApplicationMode.DEVELOPMENT)

    @property
    def is_dev(self) -> bool:
        return self.MODE == ApplicationMode.DEVELOPMENT

    MINIO_HOST: str = Field(default="localhost")
    MINIO_PORT: int = Field(default=9000)
    MINIO_ACCESS_KEY: str = Field(default="access_key")
    MINIO_SECRET_KEY: str = Field(default="secret")
    MINIO_BUCKET: str = Field(default="submissions")

    @property
    def s3_endpoint(self) -> str:
        """Get S3 endpoint."""
        return f"{self.MINIO_HOST}:{self.MINIO_PORT}"

    KAFKA_BOOTSTRAP_SERVERS: str = Field(default="localhost:29092")

    API_HOST: str = Field(default="localhost")
    API_PORT: int = Field(default=5000)

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


app_settings = AppSettings()
