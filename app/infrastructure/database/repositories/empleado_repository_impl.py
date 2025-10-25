from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.domain.models.empleado import Empleado
from typing import Optional, List
from app.domain.repositories.empleado_repository import EmpleadoRepository

class EmpleadoRepositoryImpl(EmpleadoRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, empleado_data: dict) -> Empleado:
        db_empleado = Empleado(**empleado_data)
        self.db.add(db_empleado)
        await self.db.commit()
        await self.db.refresh(db_empleado)
        return db_empleado

    async def get_by_id(self, id_empleado: int) -> Optional[Empleado]:
        result = await self.db.execute(
            select(Empleado).where(Empleado.id_empleado == id_empleado, Empleado.activo == True)
        )
        return result.scalar_one_or_none()

    async def update(self, id_empleado: int, empleado_data: dict) -> Optional[Empleado]:
        empleado = await self.get_by_id(id_empleado)
        if not empleado:
            return None
        for key, value in empleado_data.items():
            setattr(empleado, key, value)
        await self.db.commit()
        await self.db.refresh(empleado)
        return empleado

    async def delete(self, id_empleado: int) -> bool:
        empleado = await self.get_by_id(id_empleado)
        if not empleado:
            return False
        empleado.activo = False
        await self.db.commit()
        return True

    async def get_all(self) -> List[Empleado]:
        result = await self.db.execute(
            select(Empleado).where(Empleado.activo == True)
        )
        return result.scalars().all()
    
    async def get_all_by_empresa(self, id_empresa: int) -> List[Empleado]:
        result = await self.db.execute(
            select(Empleado).where(Empleado.activo == True, Empleado.id_empresa == id_empresa)
        )
        return result.scalars().all()

    async def get_all_by_gimnasio(self, id_gimnasio: int) -> List[Empleado]:
        result = await self.db.execute(
            select(Empleado).where(Empleado.activo == True, Empleado.id_gimnasio == id_gimnasio)
        )
        return result.scalars().all()

    async def get_by_correo(self, correo: str) -> Optional[Empleado]:
        query = select(Empleado).where(Empleado.correo == correo)
        result = await self.db.execute(query)
        empleado = result.scalars().first()
        return empleado

    async def get_by_cedula(self, cedula: str) -> Optional[Empleado]:
        query = select(Empleado).where(Empleado.cedula == cedula)
        result = await self.db.execute(query)
        empleado = result.scalars().first()
        return empleado
