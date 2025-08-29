import redis
import asyncio
from fastapi import HTTPException, Request
from app.core.config import settings
import time

class RateLimiter:
    def __init__(self):
        try:
            self.redis_client = redis.Redis.from_url(settings.redis_url)
            self.redis_client.ping()
            print("Conexión Redis Exitosa")
        except Exception as e:
            print(f"Conexión Redis Falidda: {e}")
            self.redis_client = None
            self.memory_storage = {}
        
        self.rate_limit = settings.rate_limit_per_minute
        self.window_size = 60

    async def check_rate_limit(self, request: Request):
        client_ip = request.client.host
        key = f"rate_limit:{client_ip}"
        
        current_time = time.time()
        
        if self.redis_client:
            try:
                window_start = current_time - self.window_size
                
                self.redis_client.zremrangebyscore(key, 0, window_start)
                
                request_count = self.redis_client.zcard(key)
                
                if request_count >= self.rate_limit:
                    raise HTTPException(status_code=429, detail="Limite de peticiones excedidas")
                
                self.redis_client.zadd(key, {str(current_time): current_time})
                self.redis_client.expire(key, self.window_size)
                
            except redis.RedisError as e:
                print(f"Error Redis: {e}. Volviendo a la memoria.")
                await self._check_memory_rate_limit(key, current_time)
        else:
            # Usar memoria si Redis no está disponible
            await self._check_memory_rate_limit(key, current_time)

    async def _check_memory_rate_limit(self, key: str, current_time: float):
        if key not in self.memory_storage:
            self.memory_storage[key] = []
        
        # Remover solicitudes antiguas
        window_start = current_time - self.window_size
        self.memory_storage[key] = [t for t in self.memory_storage[key] if t > window_start]
        
        # Verificar límite
        if len(self.memory_storage[key]) >= self.rate_limit:
            raise HTTPException(status_code=429, detail="Rate limit exceeded")
        
        # Agregar nueva solicitud
        self.memory_storage[key].append(current_time)

rate_limiter = RateLimiter()

async def init_rate_limiter():
    # Inicialización simple
    pass