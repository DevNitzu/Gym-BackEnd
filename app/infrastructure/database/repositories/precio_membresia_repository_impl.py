from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.domain.models.precio_membresia import PrecioMembresia
from typing import Optional, List
from app.domain.repositories.precio_membresia_repository import PrecioMembresiaRepository

class PrecioMembresiaRepositoryImpl(PrecioMembresiaRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, precio_membresia_data: dict) -> PrecioMembresia:
        db_precio_membresia = PrecioMembresia(**precio_membresia_data)
        self.db.add(db_precio_membresia)
        await self.db.commit()
        await self.db.refresh(db_precio_membresia)
        return db_precio_membresia

    async def get_by_id(self, id_precio_membresia: int) -> Optional[PrecioMembresia]:
        result = await self.db.execute(
            select(PrecioMembresia).where(PrecioMembresia.id_precio_membresia == id_precio_membresia, PrecioMembresia.activo == True)
        )
        return result.scalar_one_or_none()

    async def update(self, id_precio_membresia: int, precio_membresia_data: dict) -> Optional[PrecioMembresia]:
        precio_membresia = await self.get_by_id(id_precio_membresia)
        if not precio_membresia:
            return None
        for key, value in precio_membresia_data.items():
            setattr(precio_membresia, key, value)
        await self.db.commit()
        await self.db.refresh(precio_membresia)
        return precio_membresia

    async def delete(self, id_precio_membresia: int) -> bool:
        precio_membresia = await self.get_by_id(id_precio_membresia)
        if not precio_membresia:
            return False
        precio_membresia.activo = False
        await self.db.commit()
        return True

    async def get_all(self, id_gimnasio: int) -> List[PrecioMembresia]:
        result = await self.db.execute(
            select(PrecioMembresia).where(PrecioMembresia.activo == True, PrecioMembresia.id_gimnasio == id_gimnasio)
        )
        return result.scalars().all()
