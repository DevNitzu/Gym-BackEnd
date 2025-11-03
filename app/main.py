from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from app.core.config import settings
from app.infrastructure.api.web import clientes, modulos, empresas, gimnasios, tipos_empleado, empleados, horarios_gimnasio, precio_membresia, estados_pago, metodo_pago, membresias, empleados_asignacion, asistencias, empleados_dto
from app.core.base import Base, engine
from app.core.rate_limiter import init_rate_limiter
from app.core.cloudinary_init import init_cloudinary
from app.infrastructure.scheduler.scheduler import start_scheduler

# Crear la app
app = FastAPI(
    title="FastAPI Hexagonal Architecture",
    description="API with hexagonal architecture and MySQL",
    version="1.0.0"
)

# Configuración de CORS (permitir frontend en otro dominio/puerto)
origins = [
    "http://localhost:3000",  # ejemplo frontend local
    "https://midominio.com"   # tu dominio de producción
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup event
@app.on_event("startup")
async def startup():
    # Crear tablas si no usas migraciones (Alembic)
    # Base.metadata.create_all(bind=engine)
    
    # Inicializar rate limiter
    start_scheduler()
    await init_rate_limiter()

# Health check de la DB
@app.get("/health/db", tags=["health"])
def check_db_connection():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection error: {str(e)}")

# Cloudinary inicializacion
init_cloudinary()
# Rutas de la API
#Principales
app.include_router(clientes.router, prefix="/api/v1", tags=["clientes"])
app.include_router(modulos.router, prefix="/api/v1", tags=["modulos"])
app.include_router(empresas.router, prefix="/api/v1", tags=["empresas"])
app.include_router(gimnasios.router, prefix="/api/v1", tags=["gimnasios"])
app.include_router(tipos_empleado.router, prefix="/api/v1", tags=["tipos_empleado"])
app.include_router(empleados.router, prefix="/api/v1", tags=["empleados"])
app.include_router(horarios_gimnasio.router, prefix="/api/v1", tags=["horarios_gimnasio"])
app.include_router(precio_membresia.router, prefix="/api/v1", tags=["precio_membresia"])
app.include_router(estados_pago.router, prefix="/api/v1", tags=["estados_pago"])
app.include_router(metodo_pago.router, prefix="/api/v1", tags=["metodo_pago"])
app.include_router(membresias.router, prefix="/api/v1", tags=["membresias"])
app.include_router(membresias.router, prefix="/api/v1", tags=["membresias"])
app.include_router(empleados_asignacion.router, prefix="/api/v1", tags=["empleados_asignacion"])
app.include_router(asistencias.router, prefix="/api/v1", tags=["asistencias"])
# DTOs
app.include_router(empleados_dto.router, prefix="/api/v1", tags=["empleados_dto"])
# Endpoint raíz
@app.get("/")
async def root():
    return {"message": "FastAPI Hexagonal Architecture API"}
