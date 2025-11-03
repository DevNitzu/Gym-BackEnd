from app.domain.repositories.asistencia_repository import AsistenciaRepository
from app.application.schemas.asistencia_schema import AsistenciaBase, AsistenciaUpdate, AsistenciaInDB
from typing import Optional, List

class AsistenciaService:
    def __init__(self, asistencia_repository: AsistenciaRepository):
        self.asistencia_repository = asistencia_repository

    async def create_asistencia(self, asistencia_data: AsistenciaBase) -> AsistenciaInDB:
        asistencia_dict = asistencia_data.model_dump()
        asistencia_db = await self.asistencia_repository.create(asistencia_dict)

        return AsistenciaInDB.model_validate(asistencia_db)

    async def update_asistencia(self, id_asistencia: int, asistencia_data: AsistenciaUpdate) -> Optional[AsistenciaInDB]:
        updated_db = await self.asistencia_repository.update(
            id_asistencia,
            asistencia_data.model_dump(exclude_unset=True)
        )
        if not updated_db:
            return None
        return AsistenciaInDB.model_validate(updated_db)

    async def delete_asistencia(self, id_asistencia: int) -> bool:
        return await self.asistencia_repository.delete(id_asistencia)

    async def get_asistencia(self, id_asistencia: int) -> Optional[AsistenciaInDB]:
        asistencia_db = await self.asistencia_repository.get_by_id(id_asistencia)
        if not asistencia_db:
            return None
        return AsistenciaInDB.model_validate(asistencia_db)

    async def get_all_asistencias(self) -> List[AsistenciaInDB]:
        asistencias_db = await self.asistencia_repository.get_all()
        return [AsistenciaInDB.model_validate(m) for m in asistencias_db]
