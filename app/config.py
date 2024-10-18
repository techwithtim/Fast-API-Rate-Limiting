from pydantic_settings import BaseSettings, SettingsConfigDict
from slowapi import Limiter
from slowapi.util import get_remote_address
from dotenv import load_dotenv
load_dotenv()

class Settings(BaseSettings):
    # Secret key for JWT encoding/decoding
    SECRET_KEY: str = "key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Redis configuration
    REDIS_HOST: str = 'localhost'
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0

    # Rate limiter configuration
    RATE_LIMIT_STORAGE_URI: str = "redis://{redis_host}:{redis_port}"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def rate_limit_storage_uri(self) -> str:
        return self.RATE_LIMIT_STORAGE_URI.format(redis_host=self.REDIS_HOST, redis_port=self.REDIS_PORT)

    
# Create a global instance of the Settings
settings = Settings()

limiter = Limiter(
    key_func=get_remote_address,
    storage_uri=settings.rate_limit_storage_uri
)