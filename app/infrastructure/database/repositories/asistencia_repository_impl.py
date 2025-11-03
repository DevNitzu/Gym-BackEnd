from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.domain.models.asistencia import Asistencia
from typing import Optional, List
from app.domain.repositories.asistencia_repository import AsistenciaRepository

class AsistenciaRepositoryImpl(AsistenciaRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, asistencia_data: dict) -> Asistencia:
        db_asistencia = Asistencia(**asistencia_data)
        self.db.add(db_asistencia)
        await self.db.commit()
        await self.db.refresh(db_asistencia)
        return db_asistencia

    async def get_by_id(self, id_asistencia: int) -> Optional[Asistencia]:
        result = await self.db.execute(
            select(Asistencia).where(Asistencia.id_asistencia == id_asistencia, Asistencia.activo == True)
        )
        return result.scalar_one_or_none()

    async def update(self, id_asistencia: int, asistencia_data: dict) -> Optional[Asistencia]:
        asistencia = await self.get_by_id(id_asistencia)
        if not asistencia:
            return None
        for key, value in asistencia_data.items():
            setattr(asistencia, key, value)
        await self.db.commit()
        await self.db.refresh(asistencia)
        return asistencia

    async def delete(self, id_asistencia: int) -> bool:
        asistencia = await self.get_by_id(id_asistencia)
        if not asistencia:
            return False
        asistencia.activo = False
        await self.db.commit()
        return True

    async def get_all(self) -> List[Asistencia]:
        result = await self.db.execute(
            select(Asistencia).where(Asistencia.activo == True)
        )
        return result.scalars().all()
