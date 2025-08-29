from pydantic_settings import BaseSettings
from urllib.parse import quote_plus

class Settings(BaseSettings):
    # Database
    mysql_host: str
    mysql_port: int = 3306
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
    
    class Config:
        env_file = ".env"
    
    @property
    def database_url(self) -> str:
        encoded_password = quote_plus(self.mysql_password)
        return f"mysql+pymysql://{self.mysql_user}:{encoded_password}@{self.mysql_host}:{self.mysql_port}/{self.mysql_db}"

settings = Settings()