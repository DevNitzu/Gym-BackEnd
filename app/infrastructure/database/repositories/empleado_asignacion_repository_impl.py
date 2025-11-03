from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.domain.models.empleado_asignacion import EmpleadoAsignacion
from typing import Optional, List
from app.domain.repositories.empleado_asignacion_repository import EmpleadoAsignacionRepository

from app.domain.models.empresa import Empresa
from app.domain.models.gimnasio import Gimnasio
from app.domain.models.tipo_empleado import TipoEmpleado

class EmpleadoAsignacionRepositoryImpl(EmpleadoAsignacionRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, empleado_asignacion_data: dict) -> EmpleadoAsignacion:
        db_empleado_asignacion = EmpleadoAsignacion(**empleado_asignacion_data)
        self.db.add(db_empleado_asignacion)
        await self.db.commit()
        await self.db.refresh(db_empleado_asignacion)
        return db_empleado_asignacion

    async def get_by_id(self, id_empleado_asignacion: int) -> Optional[EmpleadoAsignacion]:
        result = await self.db.execute(
            select(EmpleadoAsignacion).where(EmpleadoAsignacion.id_empleado_asignacion == id_empleado_asignacion, EmpleadoAsignacion.activo == True)
        )
        return result.scalar_one_or_none()

    async def update(self, id_empleado_asignacion: int, empleado_asignacion_data: dict) -> Optional[EmpleadoAsignacion]:
        empleado_asignacion = await self.get_by_id(id_empleado_asignacion)
        if not empleado_asignacion:
            return None
        for key, value in empleado_asignacion_data.items():
            setattr(empleado_asignacion, key, value)
        await self.db.commit()
        await self.db.refresh(empleado_asignacion)
        return empleado_asignacion

    async def delete(self, id_empleado_asignacion: int) -> bool:
        empleado_asignacion = await self.get_by_id(id_empleado_asignacion)
        if not empleado_asignacion:
            return False
        empleado_asignacion.activo = False
        await self.db.commit()
        return True

    async def get_all(self) -> List[EmpleadoAsignacion]:
        result = await self.db.execute(
            select(EmpleadoAsignacion).where(EmpleadoAsignacion.activo == True)
        )
        return result.scalars().all()
    
    # Auxiliares DTO

    async def get_all_empleados_asignaciones_by_empresa(self, id_empresa: int):
        stmt = (
            select(
                EmpleadoAsignacion.id_empleado,
                EmpleadoAsignacion.id_empresa,
                Empresa.nombre.label("nombre_empresa"),
                EmpleadoAsignacion.id_gimnasio,
                Gimnasio.nombre.label("nombre_gimnasio"),
                EmpleadoAsignacion.id_tipo_empleado,
                TipoEmpleado.nombre.label("tipo_empleado_nombre"),
                EmpleadoAsignacion.activo,
                EmpleadoAsignacion.pertenece_empresa,
            )
            .join(Empresa, EmpleadoAsignacion.id_empresa == Empresa.id_empresa)
            .join(Gimnasio, EmpleadoAsignacion.id_gimnasio == Gimnasio.id_gimnasio)
            .join(TipoEmpleado, EmpleadoAsignacion.id_tipo_empleado == TipoEmpleado.id_tipo_empleado)
            .where(EmpleadoAsignacion.id_empresa == id_empresa, EmpleadoAsignacion.pertenece_empresa == True)
        )
        result = await self.db.execute(stmt)
        return result.all()
    
    async def get_all_empleados_asignaciones_by_gimnasio(self, id_gimnasio: int) -> List[EmpleadoAsignacion]:
        stmt = (
            select(
                EmpleadoAsignacion.id_empleado,
                EmpleadoAsignacion.id_empresa,
                Empresa.nombre.label("nombre_empresa"),
                EmpleadoAsignacion.id_gimnasio,
                Gimnasio.nombre.label("nombre_gimnasio"),
                EmpleadoAsignacion.id_tipo_empleado,
                TipoEmpleado.nombre.label("tipo_empleado_nombre"),
                EmpleadoAsignacion.activo,
                EmpleadoAsignacion.pertenece_empresa,
            )
            .join(Empresa, EmpleadoAsignacion.id_empresa == Empresa.id_empresa)
            .join(Gimnasio, EmpleadoAsignacion.id_gimnasio == Gimnasio.id_gimnasio)
            .join(TipoEmpleado, EmpleadoAsignacion.id_tipo_empleado == TipoEmpleado.id_tipo_empleado)
            .where(EmpleadoAsignacion.id_gimnasio == id_gimnasio, EmpleadoAsignacion.pertenece_empresa == True)
        )
        result = await self.db.execute(stmt)
        return result.all()
    
    async def get_empleado_asignacion_info(self, id_empleado: int) -> List[EmpleadoAsignacion]:
        stmt = (
            select(
                EmpleadoAsignacion.id_empleado,
                EmpleadoAsignacion.id_empresa,
                Empresa.nombre.label("nombre_empresa"),
                EmpleadoAsignacion.id_gimnasio,
                Gimnasio.nombre.label("nombre_gimnasio"),
                EmpleadoAsignacion.id_tipo_empleado,
                TipoEmpleado.nombre.label("tipo_empleado_nombre"),
                EmpleadoAsignacion.activo,
                EmpleadoAsignacion.pertenece_empresa,
            )
            .join(Empresa, EmpleadoAsignacion.id_empresa == Empresa.id_empresa)
            .join(Gimnasio, EmpleadoAsignacion.id_gimnasio == Gimnasio.id_gimnasio)
            .join(TipoEmpleado, EmpleadoAsignacion.id_tipo_empleado == TipoEmpleado.id_tipo_empleado)
            .where(EmpleadoAsignacion.id_empleado == id_empleado, EmpleadoAsignacion.pertenece_empresa == True)
        )
        result = await self.db.execute(stmt)
        return result.all()
