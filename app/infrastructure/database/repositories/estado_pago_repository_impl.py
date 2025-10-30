from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.domain.models.estado_pago import EstadoPago
from typing import Optional, List
from app.domain.repositories.estado_pago_repository import EstadoPagoRepository

class EstadoPagoRepositoryImpl(EstadoPagoRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, estado_pago_data: dict) -> EstadoPago:
        db_estado_pago = EstadoPago(**estado_pago_data)
        self.db.add(db_estado_pago)
        await self.db.commit()
        await self.db.refresh(db_estado_pago)
        return db_estado_pago

    async def get_by_id(self, id_estado_pago: int) -> Optional[EstadoPago]:
        result = await self.db.execute(
            select(EstadoPago).where(EstadoPago.id_estado_pago == id_estado_pago, EstadoPago.activo == True)
        )
        return result.scalar_one_or_none()

    async def update(self, id_estado_pago: int, estado_pago_data: dict) -> Optional[EstadoPago]:
        estado_pago = await self.get_by_id(id_estado_pago)
        if not estado_pago:
            return None
        for key, value in estado_pago_data.items():
            setattr(estado_pago, key, value)
        await self.db.commit()
        await self.db.refresh(estado_pago)
        return estado_pago

    async def delete(self, id_estado_pago: int) -> bool:
        estado_pago = await self.get_by_id(id_estado_pago)
        if not estado_pago:
            return False
        estado_pago.activo = False
        await self.db.commit()
        return True

    async def get_all(self) -> List[EstadoPago]:
        result = await self.db.execute(
            select(EstadoPago).where(EstadoPago.activo == True)
        )
        return result.scalars().all()
