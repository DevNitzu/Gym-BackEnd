from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.domain.models.membresia import Membresia
from typing import Optional, List
from app.domain.repositories.membresia_repository import MembresiaRepository

class MembresiaRepositoryImpl(MembresiaRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, membresia_data: dict) -> Membresia:
        db_membresia = Membresia(**membresia_data)
        self.db.add(db_membresia)
        await self.db.commit()
        await self.db.refresh(db_membresia)
        return db_membresia

    async def get_by_id(self, id_membresia: int) -> Optional[Membresia]:
        result = await self.db.execute(
            select(Membresia).where(Membresia.id_membresia == id_membresia, Membresia.activo == True)
        )
        return result.scalar_one_or_none()

    async def update(self, id_membresia: int, membresia_data: dict) -> Optional[Membresia]:
        membresia = await self.get_by_id(id_membresia)
        if not membresia:
            return None
        for key, value in membresia_data.items():
            setattr(membresia, key, value)
        await self.db.commit()
        await self.db.refresh(membresia)
        return membresia

    async def delete(self, id_membresia: int) -> bool:
        membresia = await self.get_by_id(id_membresia)
        if not membresia:
            return False
        membresia.activo = False
        await self.db.commit()
        return True

    async def get_all(self, id_gimnasio: int) -> List[Membresia]:
        result = await self.db.execute(
            select(Membresia).where(Membresia.activo == True, Membresia.id_gimnasio == id_gimnasio)
        )
        return result.scalars().all()
    
    # Jobs

    async def expire_membresias(self, current_date) -> int:
        result = await self.db.execute(
            select(Membresia).where(Membresia.fecha_expiracion < current_date, Membresia.activo == True, Membresia.expirado == False)
        )
        expired_membresias = result.scalars().all()
        for membresia in expired_membresias:
            membresia.expirado = True
        await self.db.commit()
        return len(expired_membresias)
