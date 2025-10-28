from app.domain.repositories.precio_membresia_repository import PrecioMembresiaRepository
from app.application.schemas.precio_membresia_schema import PrecioMembresiaBase, PrecioMembresiaUpdate, PrecioMembresiaInDB
from typing import Optional, List

class PrecioMembresiaService:
    def __init__(self, precio_membresia_repository: PrecioMembresiaRepository):
        self.precio_membresia_repository = precio_membresia_repository

    async def create_precio_membresia(self, precio_membresia_data: PrecioMembresiaBase) -> PrecioMembresiaInDB:
        precio_membresia_dict = precio_membresia_data.model_dump()
        precio_membresia_db = await self.precio_membresia_repository.create(precio_membresia_dict)

        return PrecioMembresiaInDB.model_validate(precio_membresia_db)

    async def update_precio_membresia(self, id_precio_membresia: int, precio_membresia_data: PrecioMembresiaUpdate) -> Optional[PrecioMembresiaInDB]:
        updated_db = await self.precio_membresia_repository.update(
            id_precio_membresia,
            precio_membresia_data.model_dump(exclude_unset=True)
        )
        if not updated_db:
            return None
        return PrecioMembresiaInDB.model_validate(updated_db)

    async def delete_precio_membresia(self, id_precio_membresia: int) -> bool:
        return await self.precio_membresia_repository.delete(id_precio_membresia)

    async def get_precio_membresia(self, id_precio_membresia: int) -> Optional[PrecioMembresiaInDB]:
        precio_membresia_db = await self.precio_membresia_repository.get_by_id(id_precio_membresia)
        if not precio_membresia_db:
            return None
        return PrecioMembresiaInDB.model_validate(precio_membresia_db)

    async def get_all_precio_membresias(self, id_gimnasio: int) -> List[PrecioMembresiaInDB]:
        precio_membresias_db = await self.precio_membresia_repository.get_all(id_gimnasio)
        return [PrecioMembresiaInDB.model_validate(m) for m in precio_membresias_db]