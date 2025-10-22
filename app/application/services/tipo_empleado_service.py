from app.domain.repositories.tipo_empleado_repository import TipoEmpleadoRepository
from app.application.schemas.tipo_empleado_schema import TipoEmpleadoBase, TipoEmpleadoUpdate, TipoEmpleadoInDB
from typing import Optional, List

class TipoEmpleadoService:
    def __init__(self, tipo_empleado_repository: TipoEmpleadoRepository):
        self.tipo_empleado_repository = tipo_empleado_repository

    async def create_tipo_empleado(self, tipo_empleado_data: TipoEmpleadoBase) -> TipoEmpleadoInDB:
        tipo_empleado_dict = tipo_empleado_data.model_dump()
        tipo_empleado_db = await self.tipo_empleado_repository.create(tipo_empleado_dict)

        return TipoEmpleadoInDB.model_validate(tipo_empleado_db)

    async def update_tipo_empleado(self, id_tipo_empleado: int, tipo_empleado_data: TipoEmpleadoUpdate) -> Optional[TipoEmpleadoInDB]:
        updated_db = await self.tipo_empleado_repository.update(
            id_tipo_empleado,
            tipo_empleado_data.model_dump(exclude_unset=True)
        )
        if not updated_db:
            return None
        return TipoEmpleadoInDB.model_validate(updated_db)

    async def delete_tipo_empleado(self, id_tipo_empleado: int) -> bool:
        return await self.tipo_empleado_repository.delete(id_tipo_empleado)

    async def get_tipo_empleado(self, id_tipo_empleado: int) -> Optional[TipoEmpleadoInDB]:
        tipo_empleado_db = await self.tipo_empleado_repository.get_by_id(id_tipo_empleado)
        if not tipo_empleado_db:
            return None
        return TipoEmpleadoInDB.model_validate(tipo_empleado_db)

    async def get_all_tipo_empleados(self) -> List[TipoEmpleadoInDB]:
        tipo_empleados_db = await self.tipo_empleado_repository.get_all()
        return [TipoEmpleadoInDB.model_validate(m) for m in tipo_empleados_db]