from functools import wraps
from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.security import verify_token
from app.core.rate_limiter import rate_limiter

security = HTTPBearer()


# ======================================================
# 1. Decorador para endpoints públicos (solo rate-limit)
# ======================================================
def public_endpoint(func):
    @wraps(func)
    async def wrapper(request: Request, *args, **kwargs):

        # Proteccion DDoS / Rate-limit opcional
        try:
            await rate_limiter.check_rate_limit(request)
        except Exception as e:
            print(f"[RateLimit] {e}")

        return await func(request, *args, **kwargs)

    return wrapper


# ======================================================
# 2. JWT obligatorio: verify_token() + payload en request
# ======================================================
def auth_required(func):
    @wraps(func)
    async def wrapper(request: Request, *args, **kwargs):

        # Rate-limit opcional
        try:
            await rate_limiter.check_rate_limit(request)
        except Exception as e:
            print(f"[RateLimit] {e}")

        # Extraer header Authorization
        try:
            credentials: HTTPAuthorizationCredentials = await security(request)
            token = credentials.credentials
        except Exception:
            raise HTTPException(status_code=401, detail="Token requerido")

        # Verificar token y decodificar
        payload = verify_token(token)
        if not payload:
            raise HTTPException(status_code=401, detail="Token inválido")

        # Guardar payload para siguientes decoradores
        request.state.user = payload

        return await func(request, *args, **kwargs)

    return wrapper


# ======================================================
# 3. Validar tipo de usuario dentro del token: cliente / empleado
# ======================================================
def user_type_required(user_type: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):

            payload = getattr(request.state, "user", None)
            if not payload:
                raise HTTPException(401, "Token inválido o faltante")
            print("User Type in Payload:", payload.get("type"))
            if payload.get("type") != user_type:
                raise HTTPException(
                    status_code=403,
                    detail=f"Este endpoint es solo para {user_type}s"
                )

            return await func(request, *args, **kwargs)

        return wrapper
    return decorator