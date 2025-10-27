from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.domain.models.horario_gimnasio import HorarioGimnasio
from typing import Optional, List
from app.domain.repositories.horario_gimnasio_repository import HorarioGimnasioRepository

class HorarioGimnasioRepositoryImpl(HorarioGimnasioRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, horario_gimnasio_data: dict) -> HorarioGimnasio:
        db_horario_gimnasio = HorarioGimnasio(**horario_gimnasio_data)
        self.db.add(db_horario_gimnasio)
        await self.db.commit()
        await self.db.refresh(db_horario_gimnasio)
        return db_horario_gimnasio

    async def get_by_id(self, id_horario_gimnasio: int) -> Optional[HorarioGimnasio]:
        result = await self.db.execute(
            select(HorarioGimnasio).where(HorarioGimnasio.id_horario_gimnasio == id_horario_gimnasio, HorarioGimnasio.activo == True)
        )
        return result.scalar_one_or_none()

    async def update(self, id_horario_gimnasio: int, horario_gimnasio_data: dict) -> Optional[HorarioGimnasio]:
        horario_gimnasio = await self.get_by_id(id_horario_gimnasio)
        if not horario_gimnasio:
            return None
        for key, value in horario_gimnasio_data.items():
            setattr(horario_gimnasio, key, value)
        await self.db.commit()
        await self.db.refresh(horario_gimnasio)
        return horario_gimnasio

    async def delete(self, id_horario_gimnasio: int) -> bool:
        horario_gimnasio = await self.get_by_id(id_horario_gimnasio)
        if not horario_gimnasio:
            return False
        horario_gimnasio.activo = False
        await self.db.commit()
        return True

    async def get_all(self, id_gimnasio: int) -> List[HorarioGimnasio]:
        result = await self.db.execute(
            select(HorarioGimnasio).where(HorarioGimnasio.activo == True, HorarioGimnasio.id_gimnasio == id_gimnasio)
        )
        return result.scalars().all()
