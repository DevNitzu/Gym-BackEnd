from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.domain.models.modulo import Modulo
from typing import Optional, List
from app.domain.repositories.modulo_repository import ModuloRepository

class ModuloRepositoryImpl(ModuloRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, modulo_data: dict) -> Modulo:
        db_modulo = Modulo(**modulo_data)
        self.db.add(db_modulo)
        await self.db.commit()
        await self.db.refresh(db_modulo)
        return db_modulo

    async def get_by_id(self, id_modulo: int) -> Optional[Modulo]:
        result = await self.db.execute(
            select(Modulo).where(Modulo.id_modulo == id_modulo, Modulo.activo == True)
        )
        return result.scalar_one_or_none()

    async def update(self, id_modulo: int, modulo_data: dict) -> Optional[Modulo]:
        modulo = await self.get_by_id(id_modulo)
        if not modulo:
            return None
        for key, value in modulo_data.items():
            setattr(modulo, key, value)
        await self.db.commit()
        await self.db.refresh(modulo)
        return modulo

    async def delete(self, id_modulo: int) -> bool:
        modulo = await self.get_by_id(id_modulo)
        if not modulo:
            return False
        modulo.activo = False
        await self.db.commit()
        return True

    async def get_all(self) -> List[Modulo]:
        result = await self.db.execute(
            select(Modulo).where(Modulo.activo == True)
        )
        return result.scalars().all()
