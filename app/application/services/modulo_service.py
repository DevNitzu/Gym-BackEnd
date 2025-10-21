from app.domain.repositories.modulo_repository import ModuloRepository
from app.application.schemas.modulo_schema import ModuloBase, ModuloUpdate, ModuloInDB
from typing import Optional, List

class ModuloService:
    def __init__(self, modulo_repository: ModuloRepository):
        self.modulo_repository = modulo_repository

    async def create_modulo(self, modulo_data: ModuloBase) -> ModuloInDB:
        modulo_dict = modulo_data.model_dump()
        modulo_db = await self.modulo_repository.create(modulo_dict)

        return ModuloInDB.model_validate(modulo_db)

    async def update_modulo(self, id_modulo: int, modulo_data: ModuloUpdate) -> Optional[ModuloInDB]:
        updated_db = await self.modulo_repository.update(
            id_modulo,
            modulo_data.model_dump(exclude_unset=True)
        )
        if not updated_db:
            return None
        return ModuloInDB.model_validate(updated_db)

    async def delete_modulo(self, id_modulo: int) -> bool:
        return await self.modulo_repository.delete(id_modulo)

    async def get_modulo(self, id_modulo: int) -> Optional[ModuloInDB]:
        modulo_db = await self.modulo_repository.get_by_id(id_modulo)
        if not modulo_db:
            return None
        return ModuloInDB.model_validate(modulo_db)

    async def get_all_modulos(self) -> List[ModuloInDB]:
        modulos_db = await self.modulo_repository.get_all()
        return [ModuloInDB.model_validate(m) for m in modulos_db]