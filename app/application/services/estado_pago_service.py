from app.domain.repositories.estado_pago_repository import EstadoPagoRepository
from app.application.schemas.estado_pago_schema import EstadoPagoBase, EstadoPagoUpdate, EstadoPagoInDB
from typing import Optional, List

class EstadoPagoService:
    def __init__(self, estado_pago_repository: EstadoPagoRepository):
        self.estado_pago_repository = estado_pago_repository

    async def create_estado_pago(self, estado_pago_data: EstadoPagoBase) -> EstadoPagoInDB:
        estado_pago_dict = estado_pago_data.model_dump()
        estado_pago_db = await self.estado_pago_repository.create(estado_pago_dict)

        return EstadoPagoInDB.model_validate(estado_pago_db)

    async def update_estado_pago(self, id_estado_pago: int, estado_pago_data: EstadoPagoUpdate) -> Optional[EstadoPagoInDB]:
        updated_db = await self.estado_pago_repository.update(
            id_estado_pago,
            estado_pago_data.model_dump(exclude_unset=True)
        )
        if not updated_db:
            return None
        return EstadoPagoInDB.model_validate(updated_db)

    async def delete_estado_pago(self, id_estado_pago: int) -> bool:
        return await self.estado_pago_repository.delete(id_estado_pago)

    async def get_estado_pago(self, id_estado_pago: int) -> Optional[EstadoPagoInDB]:
        estado_pago_db = await self.estado_pago_repository.get_by_id(id_estado_pago)
        if not estado_pago_db:
            return None
        return EstadoPagoInDB.model_validate(estado_pago_db)

    async def get_all_estado_pagos(self) -> List[EstadoPagoInDB]:
        estado_pagos_db = await self.estado_pago_repository.get_all()
        return [EstadoPagoInDB.model_validate(m) for m in estado_pagos_db]