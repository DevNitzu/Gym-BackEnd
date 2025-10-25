from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.domain.models.gimnasio import Gimnasio
from typing import Optional, List
from app.domain.repositories.gimnasio_repository import GimnasioRepository

class GimnasioRepositoryImpl(GimnasioRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, gimnasio_data: dict) -> Gimnasio:
        db_gimnasio = Gimnasio(**gimnasio_data)
        self.db.add(db_gimnasio)
        await self.db.commit()
        await self.db.refresh(db_gimnasio)
        return db_gimnasio

    async def get_by_id(self, id_gimnasio: int) -> Optional[Gimnasio]:
        result = await self.db.execute(
            select(Gimnasio).where(Gimnasio.id_gimnasio == id_gimnasio, Gimnasio.activo == True)
        )
        return result.scalar_one_or_none()

    async def update(self, id_gimnasio: int, gimnasio_data: dict) -> Optional[Gimnasio]:
        gimnasio = await self.get_by_id(id_gimnasio)
        if not gimnasio:
            return None
        for key, value in gimnasio_data.items():
            setattr(gimnasio, key, value)
        await self.db.commit()
        await self.db.refresh(gimnasio)
        return gimnasio

    async def delete(self, id_gimnasio: int) -> bool:
        gimnasio = await self.get_by_id(id_gimnasio)
        if not gimnasio:
            return False
        gimnasio.activo = False
        await self.db.commit()
        return True

    async def get_all(self, id_empresa: int) -> List[Gimnasio]:
        result = await self.db.execute(
            select(Gimnasio).where(Gimnasio.activo == True, Gimnasio.id_empresa == id_empresa)
        )
        return result.scalars().all()
