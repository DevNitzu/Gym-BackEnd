from functools import wraps
from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.security import verify_token
from app.core.rate_limiter import rate_limiter

security = HTTPBearer()


# ======================================================
# 1. ENDPOINT PÚBLICO (rate-limit)
# ======================================================
def public_endpoint(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        # Obtener request sin alterar la firma
        request: Request = kwargs.get("request") or args[0]

        try:
            await rate_limiter.check_rate_limit(request)
        except Exception as e:
            print(f"[RateLimit] {e}")

        return await func(*args, **kwargs)

    return wrapper


# ======================================================
# 2. JWT obligatorio
# ======================================================
def auth_required(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        request: Request = kwargs.get("request") or args[0]

        # rate limit
        try:
            await rate_limiter.check_rate_limit(request)
        except Exception as e:
            print(f"[RateLimit] {e}")

        # Auth Bearer
        try:
            credentials: HTTPAuthorizationCredentials = await security(request)
            token = credentials.credentials
        except Exception:
            raise HTTPException(status_code=401, detail="Token requerido")

        payload = verify_token(token)
        if not payload:
            raise HTTPException(status_code=401, detail="Token inválido")

        request.state.user = payload

        return await func(*args, **kwargs)

    return wrapper


# ======================================================
# 3. Validación del tipo de usuario
# ======================================================
def user_type_required(user_type: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request: Request = kwargs.get("request") or args[0]

            payload = getattr(request.state, "user", None)
            if not payload:
                raise HTTPException(401, "Token inválido o faltante")

            print("User Type in Payload:", payload.get("type"))

            if payload.get("type") != user_type:
                raise HTTPException(
                    status_code=403,
                    detail=f"Este endpoint es solo para {user_type}s"
                )

            return await func(*args, **kwargs)
        return wrapper
    return decorator
