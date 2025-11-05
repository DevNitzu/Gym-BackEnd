from app.domain.repositories.membresia_repository import MembresiaRepository
from app.application.schemas.membresia_schema import MembresiaBase, MembresiaUpdate, MembresiaInDB
from typing import Optional, List
from dateutil.relativedelta import relativedelta
from datetime import datetime
from zoneinfo import ZoneInfo

class MembresiaService:
    def __init__(self, membresia_repository: MembresiaRepository):
        self.membresia_repository = membresia_repository

    # Funciones privadas para cálculos
    def _calcular_fecha_expiracion(self, fecha_inicio: datetime, unidad: str, cantidad: int) -> datetime:
        if unidad == "mes":
            return fecha_inicio + relativedelta(months=cantidad)
        elif unidad == "año":
            return fecha_inicio + relativedelta(years=cantidad)
        else:
            raise ValueError("Unidad de duración inválida")

    def _calcular_precio_total(precio_unitario: float, cantidad: int, descuento: float = 0) -> float:
        return round(precio_unitario * cantidad * (1 - descuento), 2)

    # Funciones públicas del servicio

    async def create_membresia(self, membresia_data: MembresiaBase) -> MembresiaInDB:
        membresia_dict = membresia_data.model_dump()

        if not membresia_dict["unidad_duracion"] == "dia" :
            membresia_dict["fecha_expiracion"] = self._calcular_fecha_expiracion(
                membresia_dict["fecha_inicio"],
                membresia_dict["unidad_duracion"],
                membresia_dict["cantidad_duracion"]
            )

        if not membresia_dict.get("precio_total"):
            membresia_dict["precio_total"] = self._calcular_precio_total(
                membresia_dict["precio_unitario"],
                membresia_dict["cantidad_duracion"],
                membresia_dict.get("descuento", 0)
            )

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
    
    # Extra

    async def get_count_active_membresias_by_gimnasio(self, id_gimnasio: int) -> int:
        count = await self.membresia_repository.get_count_active_membresias_by_gimnasio(id_gimnasio)
        return count

    # Jobs

    async def expire_membresias(self) -> int:
        current_date = datetime.now(ZoneInfo("America/Guayaquil"))
        expired_count = await self.membresia_repository.expire_membresias(current_date)
        return expired_count
