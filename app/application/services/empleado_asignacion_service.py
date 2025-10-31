from app.domain.repositories.empleado_asignacion_repository import EmpleadoAsignacionRepository
from app.application.schemas.empleado_asignacion_schema import EmpleadoAsignacionBase, EmpleadoAsignacionUpdate, EmpleadoAsignacionInDB
from typing import Optional, List

class EmpleadoAsignacionService:
    def __init__(self, empleado_asignacion_repository: EmpleadoAsignacionRepository):
        self.empleado_asignacion_repository = empleado_asignacion_repository

    async def create_empleado_asignacion(self, empleado_asignacion_data: EmpleadoAsignacionBase) -> EmpleadoAsignacionInDB:
        empleado_asignacion_dict = empleado_asignacion_data.model_dump()
        empleado_asignacion_db = await self.empleado_asignacion_repository.create(empleado_asignacion_dict)

        return EmpleadoAsignacionInDB.model_validate(empleado_asignacion_db)

    async def update_empleado_asignacion(self, id_empleado_asignacion: int, empleado_asignacion_data: EmpleadoAsignacionUpdate) -> Optional[EmpleadoAsignacionInDB]:
        updated_db = await self.empleado_asignacion_repository.update(
            id_empleado_asignacion,
            empleado_asignacion_data.model_dump(exclude_unset=True)
        )
        if not updated_db:
            return None
        return EmpleadoAsignacionInDB.model_validate(updated_db)

    async def delete_empleado_asignacion(self, id_empleado_asignacion: int) -> bool:
        return await self.empleado_asignacion_repository.delete(id_empleado_asignacion)

    async def get_empleado_asignacion(self, id_empleado_asignacion: int) -> Optional[EmpleadoAsignacionInDB]:
        empleado_asignacion_db = await self.empleado_asignacion_repository.get_by_id(id_empleado_asignacion)
        if not empleado_asignacion_db:
            return None
        return EmpleadoAsignacionInDB.model_validate(empleado_asignacion_db)

    async def get_all_empleados_asignacion(self) -> List[EmpleadoAsignacionInDB]:
        empleado_asignacions_db = await self.empleado_asignacion_repository.get_all()
        return [EmpleadoAsignacionInDB.model_validate(m) for m in empleado_asignacions_db]