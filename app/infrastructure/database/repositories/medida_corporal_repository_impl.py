from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.domain.models.medida_corporal import MedidaCorporal
from typing import Optional, List
from app.domain.repositories.medida_corporal_repository import MedidaCorporalRepository

class MedidaCorporalRepositoryImpl(MedidaCorporalRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, medida_corporal_data: dict) -> MedidaCorporal:
        db_medida_corporal = MedidaCorporal(**medida_corporal_data)
        self.db.add(db_medida_corporal)
        await self.db.commit()
        await self.db.refresh(db_medida_corporal)
        return db_medida_corporal

    async def get_by_id(self, id_medida_corporal: int) -> Optional[MedidaCorporal]:
        result = await self.db.execute(
            select(MedidaCorporal).where(MedidaCorporal.id_medida_corporal == id_medida_corporal, MedidaCorporal.activo == True)
        )
        return result.scalar_one_or_none()

    async def update(self, id_medida_corporal: int, medida_corporal_data: dict) -> Optional[MedidaCorporal]:
        medida_corporal = await self.get_by_id(id_medida_corporal)
        if not medida_corporal:
            return None
        for key, value in medida_corporal_data.items():
            setattr(medida_corporal, key, value)
        await self.db.commit()
        await self.db.refresh(medida_corporal)
        return medida_corporal

    async def delete(self, id_medida_corporal: int) -> bool:
        medida_corporal = await self.get_by_id(id_medida_corporal)
        if not medida_corporal:
            return False
        medida_corporal.activo = False
        await self.db.commit()
        return True

    async def get_all(self) -> List[MedidaCorporal]:
        result = await self.db.execute(
            select(MedidaCorporal).where(MedidaCorporal.activo == True)
        )
        return result.scalars().all()
    
    async def get_all_by_cliente(self, id_cliente: int) -> Optional[MedidaCorporal]:
        query = select(MedidaCorporal).where(MedidaCorporal.id_cliente == id_cliente)
        result = await self.db.execute(query)
        medida_corporal = result.scalars().first()
        return medida_corporal

    async def get_last_by_cliente(self, id_cliente: int) -> Optional[MedidaCorporal]:
        query = (
            select(MedidaCorporal)
            .where(MedidaCorporal.id_cliente == id_cliente)
            .order_by(desc(MedidaCorporal.fecha_creacion))
            .limit(1)
        )
        
        result = await self.db.execute(query)
        return result.scalars().first()

