from app.domain.repositories.membresia_repository import MembresiaRepository
from app.application.schemas.membresia_schema import MembresiaBase, MembresiaUpdate, MembresiaInDB
from typing import Optional, List

class MembresiaService:
    def __init__(self, membresia_repository: MembresiaRepository):
        self.membresia_repository = membresia_repository

    async def create_membresia(self, membresia_data: MembresiaBase) -> MembresiaInDB:
        membresia_dict = membresia_data.model_dump()
        membresia_db = await self.membresia_repository.create(membresia_dict)

        return MembresiaInDB.model_validate(membresia_db)

    async def update_membresia(self, id_membresia: int, membresia_data: MembresiaUpdate) -> Optional[MembresiaInDB]:
        updated_db = await self.membresia_repository.update(
            id_membresia,
            membresia_data.model_dump(exclude_unset=True)
        )
        if not updated_db:
            return None
        return MembresiaInDB.model_validate(updated_db)

    async def delete_membresia(self, id_membresia: int) -> bool:
        return await self.membresia_repository.delete(id_membresia)

    async def get_membresia(self, id_membresia: int) -> Optional[MembresiaInDB]:
        membresia_db = await self.membresia_repository.get_by_id(id_membresia)
        if not membresia_db:
            return None
        return MembresiaInDB.model_validate(membresia_db)

    async def get_all_membresias(self, id_gimnasio: int) -> List[MembresiaInDB]:
        membresias_db = await self.membresia_repository.get_all(id_gimnasio)
        return [MembresiaInDB.model_validate(m) for m in membresias_db]