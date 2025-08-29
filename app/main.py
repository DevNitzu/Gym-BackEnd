from fastapi import FastAPI
from app.core.config import settings
from app.infrastructure.api.routes import clientes
from app.infrastructure.database.base import Base, engine
from app.core.rate_limiter import init_rate_limiter

app = FastAPI(
    title="FastAPI Hexagonal Architecture",
    description="API with hexagonal architecture and MySQL",
    version="1.0.0"
)

# Create database tables
@app.on_event("startup")
async def startup():
    Base.metadata.create_all(bind=engine)
    await init_rate_limiter()

# Include routers
app.include_router(clientes.router, prefix="/api/v1", tags=["clientes"])

@app.get("/")
async def root():
    return {"message": "FastAPI Hexagonal Architecture API"}