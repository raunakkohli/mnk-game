from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    db_url: str = Field(..., env='DATABASE_URL')
    use_cache: bool = Field(..., env='CACHE_ENABLED')

settings = Settings()