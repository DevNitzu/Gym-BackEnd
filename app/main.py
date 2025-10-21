from fastapi import FastAPI,HTTPException
from app.core.config import settings
from app.infrastructure.api.routes import clientes,modulos, empresas
from app.infrastructure.database.base import Base, engine
from app.core.rate_limiter import init_rate_limiter
from sqlalchemy import text

app = FastAPI(
    title="FastAPI Hexagonal Architecture",
    description="API with hexagonal architecture and MySQL",
    version="1.0.0"
)

# Create database tables
@app.on_event("startup")
async def startup():
    #Base.metadata.create_all(bind=engine)
    await init_rate_limiter()

@app.get("/health/db", tags=["health"])
def check_db_connection():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection error: {str(e)}")
# Include routers
app.include_router(clientes.router, prefix="/api/v1", tags=["clientes"])
app.include_router(modulos.router, prefix="/api/v1", tags=["modulos"])
app.include_router(empresas.router, prefix="/api/v1", tags=["empresas"])

@app.get("/")
async def root():
    return {"message": "FastAPI Hexagonal Architecture API"}