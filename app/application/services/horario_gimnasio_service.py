from app.domain.repositories.horario_gimnasio_repository import HorarioGimnasioRepository
from app.application.schemas.horario_gimnasio_schema import HorarioGimnasioBase, HorarioGimnasioUpdate, HorarioGimnasioInDB
from typing import Optional, List

class HorarioGimnasioService:
    def __init__(self, horario_gimnasio_repository: HorarioGimnasioRepository):
        self.horario_gimnasio_repository = horario_gimnasio_repository

    async def create_horario_gimnasio(self, horario_gimnasio_data: HorarioGimnasioBase) -> HorarioGimnasioInDB:
        horario_gimnasio_dict = horario_gimnasio_data.model_dump()
        horario_gimnasio_db = await self.horario_gimnasio_repository.create(horario_gimnasio_dict)

        return HorarioGimnasioInDB.model_validate(horario_gimnasio_db)

    async def update_horario_gimnasio(self, id_horario_gimnasio: int, horario_gimnasio_data: HorarioGimnasioUpdate) -> Optional[HorarioGimnasioInDB]:
        updated_db = await self.horario_gimnasio_repository.update(
            id_horario_gimnasio,
            horario_gimnasio_data.model_dump(exclude_unset=True)
        )
        if not updated_db:
            return None
        return HorarioGimnasioInDB.model_validate(updated_db)

    async def delete_horario_gimnasio(self, id_horario_gimnasio: int) -> bool:
        return await self.horario_gimnasio_repository.delete(id_horario_gimnasio)

    async def get_horario_gimnasio(self, id_horario_gimnasio: int) -> Optional[HorarioGimnasioInDB]:
        horario_gimnasio_db = await self.horario_gimnasio_repository.get_by_id(id_horario_gimnasio)
        if not horario_gimnasio_db:
            return None
        return HorarioGimnasioInDB.model_validate(horario_gimnasio_db)

    async def get_all_horario_gimnasios(self, id_gimnasio: int) -> List[HorarioGimnasioInDB]:
        horario_gimnasios_db = await self.horario_gimnasio_repository.get_all(id_gimnasio)
        return [HorarioGimnasioInDB.model_validate(m) for m in horario_gimnasios_db]