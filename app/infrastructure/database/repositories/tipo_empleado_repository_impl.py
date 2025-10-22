from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.domain.models.tipo_empleado import TipoEmpleado
from typing import Optional, List
from app.domain.repositories.tipo_empleado_repository import TipoEmpleadoRepository

class TipoEmpleadoRepositoryImpl(TipoEmpleadoRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, tipo_empleado_data: dict) -> TipoEmpleado:
        db_tipo_empleado = TipoEmpleado(**tipo_empleado_data)
        self.db.add(db_tipo_empleado)
        await self.db.commit()
        await self.db.refresh(db_tipo_empleado)
        return db_tipo_empleado

    async def get_by_id(self, id_tipo: int) -> Optional[TipoEmpleado]:
        result = await self.db.execute(
            select(TipoEmpleado).where(TipoEmpleado.id_tipo == id_tipo, TipoEmpleado.activo == True)
        )
        return result.scalar_one_or_none()

    async def update(self, id_tipo: int, tipo_empleado_data: dict) -> Optional[TipoEmpleado]:
        tipo_empleado = await self.get_by_id(id_tipo)
        if not tipo_empleado:
            return None
        for key, value in tipo_empleado_data.items():
            setattr(tipo_empleado, key, value)
        await self.db.commit()
        await self.db.refresh(tipo_empleado)
        return tipo_empleado

    async def delete(self, id_tipo: int) -> bool:
        tipo_empleado = await self.get_by_id(id_tipo)
        if not tipo_empleado:
            return False
        tipo_empleado.activo = False
        await self.db.commit()
        return True

    async def get_all(self) -> List[TipoEmpleado]:
        result = await self.db.execute(
            select(TipoEmpleado).where(TipoEmpleado.activo == True)
        )
        return result.scalars().all()
