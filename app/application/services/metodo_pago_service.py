from app.domain.repositories.metodo_pago_repository import MetodoPagoRepository
from app.application.schemas.metodo_pago_schema import MetodoPagoBase, MetodoPagoUpdate, MetodoPagoInDB
from typing import Optional, List

class MetodoPagoService:
    def __init__(self, metodo_pago_repository: MetodoPagoRepository):
        self.metodo_pago_repository = metodo_pago_repository

    async def create_metodo_pago(self, metodo_pago_data: MetodoPagoBase) -> MetodoPagoInDB:
        metodo_pago_dict = metodo_pago_data.model_dump()
        metodo_pago_db = await self.metodo_pago_repository.create(metodo_pago_dict)

        return MetodoPagoInDB.model_validate(metodo_pago_db)

    async def update_metodo_pago(self, id_metodo_pago: int, metodo_pago_data: MetodoPagoUpdate) -> Optional[MetodoPagoInDB]:
        updated_db = await self.metodo_pago_repository.update(
            id_metodo_pago,
            metodo_pago_data.model_dump(exclude_unset=True)
        )
        if not updated_db:
            return None
        return MetodoPagoInDB.model_validate(updated_db)

    async def delete_metodo_pago(self, id_metodo_pago: int) -> bool:
        return await self.metodo_pago_repository.delete(id_metodo_pago)

    async def get_metodo_pago(self, id_metodo_pago: int) -> Optional[MetodoPagoInDB]:
        metodo_pago_db = await self.metodo_pago_repository.get_by_id(id_metodo_pago)
        if not metodo_pago_db:
            return None
        return MetodoPagoInDB.model_validate(metodo_pago_db)

    async def get_all_metodo_pagos(self) -> List[MetodoPagoInDB]:
        metodo_pagos_db = await self.metodo_pago_repository.get_all()
        return [MetodoPagoInDB.model_validate(m) for m in metodo_pagos_db]