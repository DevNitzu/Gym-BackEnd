from functools import wraps
from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.security import verify_token
from app.core.rate_limiter import rate_limiter

security = HTTPBearer()

def public_endpoint(func):
    @wraps(func)
    async def wrapper(request: Request, *args, **kwargs):
        try:
            await rate_limiter.check_rate_limit(request)
        except Exception as e:
            print(f"Protección DDoS activada: {e}")
        return await func(request, *args, **kwargs)
    return wrapper

def private_endpoint(func):
    @wraps(func)
    async def wrapper(request: Request, *args, **kwargs):
        try:
            await rate_limiter.check_rate_limit(request)
        except Exception as e:
            print(f"Protección DDoS activada: {e}")
        
        try:
            credentials: HTTPAuthorizationCredentials = await security(request)
            token = credentials.credentials
            payload = verify_token(token)
            if not payload:
                raise HTTPException(status_code=401, detail="Token invalido")
        except Exception as e:
            raise HTTPException(status_code=401, detail="Se requiere autorización")
        
        return await func(request, *args, **kwargs)
    return wrapper