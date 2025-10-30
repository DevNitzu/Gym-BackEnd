from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.domain.models.metodo_pago import MetodoPago
from typing import Optional, List
from app.domain.repositories.metodo_pago_repository import MetodoPagoRepository

class MetodoPagoRepositoryImpl(MetodoPagoRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, metodo_pago_data: dict) -> MetodoPago:
        db_metodo_pago = MetodoPago(**metodo_pago_data)
        self.db.add(db_metodo_pago)
        await self.db.commit()
        await self.db.refresh(db_metodo_pago)
        return db_metodo_pago

    async def get_by_id(self, id_metodo_pago: int) -> Optional[MetodoPago]:
        result = await self.db.execute(
            select(MetodoPago).where(MetodoPago.id_metodo_pago == id_metodo_pago, MetodoPago.activo == True)
        )
        return result.scalar_one_or_none()

    async def update(self, id_metodo_pago: int, metodo_pago_data: dict) -> Optional[MetodoPago]:
        metodo_pago = await self.get_by_id(id_metodo_pago)
        if not metodo_pago:
            return None
        for key, value in metodo_pago_data.items():
            setattr(metodo_pago, key, value)
        await self.db.commit()
        await self.db.refresh(metodo_pago)
        return metodo_pago

    async def delete(self, id_metodo_pago: int) -> bool:
        metodo_pago = await self.get_by_id(id_metodo_pago)
        if not metodo_pago:
            return False
        metodo_pago.activo = False
        await self.db.commit()
        return True

    async def get_all(self) -> List[MetodoPago]:
        result = await self.db.execute(
            select(MetodoPago).where(MetodoPago.activo == True)
        )
        return result.scalars().all()
