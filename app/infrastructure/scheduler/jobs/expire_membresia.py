# app/infrastructure/scheduler/jobs/expire_membresia.py
import logging
from app.core.base import get_db
from app.infrastructure.database.repositories.membresia_repository_impl import MembresiaRepositoryImpl
from app.application.services.membresia_service import MembresiaService

logger = logging.getLogger(__name__)

async def expire_membresias():
    async_gen = get_db()                  # get_db() devuelve async generator
    db = await async_gen.__anext__()      # obtener AsyncSession
    try:
        # aquí tu repo y service
        membresia_repo = MembresiaRepositoryImpl(db)
        service = MembresiaService(membresia_repo)
        count = await service.expire_membresias()
        logger.info(f"✅ {count} membresías expiradas")
    finally:
        await db.close()                   # cerrar sesión
        await async_gen.aclose()           # cerrar generator

