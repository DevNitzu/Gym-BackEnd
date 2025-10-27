from pydantic_settings import BaseSettings
from urllib.parse import quote_plus

class Settings(BaseSettings):
    # Database
    mysql_host: str
    mysql_port: int = 3307
    mysql_db: str
    mysql_user: str
    mysql_password: str
    
    # JWT
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Rate Limiting
    redis_url: str = "redis://redis:6379"
    rate_limit_per_minute: int = 10

    # Cloudinary
    cloud_name: str
    cloud_api_key: str
    cloud_api_secret: str
    
    class Config:
        env_file = ".env"
    
    @property
    def database_url(self) -> str:
        encoded_password = quote_plus(self.mysql_password)
        return f"mysql+pymysql://{self.mysql_user}:{encoded_password}@{self.mysql_host}:{self.mysql_port}/{self.mysql_db}"

    @property
    def cloudinary_config(self) -> dict:
        return {
            "cloud_name": self.cloud_name,
            "api_key": self.cloud_api_key,
            "api_secret": self.cloud_api_secret,
            "secure": True
        }
    
settings = Settings()