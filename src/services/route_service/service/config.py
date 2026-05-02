from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Настройки приложения"""
    app_name: str = "Moscow Routing API"
    app_version: str = "1.0.0"
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = False

    network_type: str = "drive"
    cache_enabled: bool = True

    max_points_per_route: int = 50
    max_batch_size: int = 10

    class Config:
        env_file = ".env"


settings = Settings()
