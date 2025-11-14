from app.domain.repositories.medida_corporal_repository import MedidaCorporalRepository
from app.application.schemas.medida_corporal_schema import MedidasCorporalesBase, MedidaCorporalUpdate, MedidaCorporalInDB
from app.core.security import get_password_hash, verify_password, create_access_token
from datetime import timedelta
from app.core.config import settings
from typing import Optional, List

class MedidaCorporalService:
    def __init__(self, medida_corporal_repository: MedidaCorporalRepository):
        self.medida_corporal_repository = medida_corporal_repository


    async def create_medida_corporal(self, medida_corporal_data: MedidasCorporalesBase) -> MedidaCorporalInDB:
        medida_corporal_dict = medida_corporal_data.model_dump()
        medida_corporal_db = await self.medida_corporal_repository.create(medida_corporal_dict)

        return MedidaCorporalInDB.model_validate(medida_corporal_db)

    async def update_medida_corporal(self, id_medida_corporal: int, medida_corporal_data: MedidaCorporalUpdate) -> Optional[MedidaCorporalInDB]:
        updated_db = await self.medida_corporal_repository.update(
            id_medida_corporal,
            medida_corporal_data.model_dump(exclude_unset=True)
        )
        if not updated_db:
            return None
        return MedidaCorporalInDB.model_validate(updated_db)

    async def delete_medida_corporal(self, id_medida_corporal: int) -> bool:
        return await self.medida_corporal_repository.delete(id_medida_corporal)

    async def get_medida_corporal(self, id_medida_corporal: int) -> Optional[MedidaCorporalInDB]:
        medida_corporal_db = await self.medida_corporal_repository.get_by_id(id_medida_corporal)
        if not medida_corporal_db:
            return None
        return MedidaCorporalInDB.model_validate(medida_corporal_db)

    async def get_all_medidas_corporales(self, id_empresa: int) -> List[MedidaCorporalInDB]:
        medida_corporals_db = await self.medida_corporal_repository.get_all(id_empresa)
        return [MedidaCorporalInDB.model_validate(m) for m in medida_corporals_db]
    
    async def get_all_medidas_coporales_by_cliente(self, id_cliente: int) -> List[MedidaCorporalInDB]:
        medida_corporals_db = await self.medida_corporal_repository.get_all_by_cliente(id_cliente)
        return [MedidaCorporalInDB.model_validate(m) for m in medida_corporals_db]
    
    async def get_last_medida_coporal_by_cliente(self, id_cliente: int) -> Optional[MedidaCorporalInDB]:
        medida_db = await self.medida_corporal_repository.get_last_by_cliente(id_cliente)

        if not medida_db:
            return None

        return MedidaCorporalInDB.model_validate(medida_db)

