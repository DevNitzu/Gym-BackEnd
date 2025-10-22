from app.domain.repositories.gimnasio_repository import GimnasioRepository
from app.application.schemas.gimnasio_schema import GimnasioBase, GimnasioUpdate, GimnasioInDB
from typing import Optional, List

class GimnasioService:
    def __init__(self, gimnasio_repository: GimnasioRepository):
        self.gimnasio_repository = gimnasio_repository

    async def create_gimnasio(self, gimnasio_data: GimnasioBase) -> GimnasioInDB:
        gimnasio_dict = gimnasio_data.model_dump()
        gimnasio_db = await self.gimnasio_repository.create(gimnasio_dict)

        return GimnasioInDB.model_validate(gimnasio_db)

    async def update_gimnasio(self, id_gimnasio: int, gimnasio_data: GimnasioUpdate) -> Optional[GimnasioInDB]:
        updated_db = await self.gimnasio_repository.update(
            id_gimnasio,
            gimnasio_data.model_dump(exclude_unset=True)
        )
        if not updated_db:
            return None
        return GimnasioInDB.model_validate(updated_db)

    async def delete_gimnasio(self, id_gimnasio: int) -> bool:
        return await self.gimnasio_repository.delete(id_gimnasio)

    async def get_gimnasio(self, id_gimnasio: int) -> Optional[GimnasioInDB]:
        gimnasio_db = await self.gimnasio_repository.get_by_id(id_gimnasio)
        if not gimnasio_db:
            return None
        return GimnasioInDB.model_validate(gimnasio_db)

    async def get_all_gimnasios(self) -> List[GimnasioInDB]:
        gimnasios_db = await self.gimnasio_repository.get_all()
        return [GimnasioInDB.model_validate(m) for m in gimnasios_db]