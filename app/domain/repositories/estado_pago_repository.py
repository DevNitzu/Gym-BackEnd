from abc import ABC, abstractmethod
from app.domain.models.estado_pago import EstadoPago
from typing import Optional, List

class EstadoPagoRepository(ABC):
    @abstractmethod
    async def create(self, estado_pago: EstadoPago) -> EstadoPago:
        pass
    
    @abstractmethod
    async def get_by_id(self, id_estado_pago: int) -> Optional[EstadoPago]:
        pass
    
    @abstractmethod
    async def update(self, id_estado_pago: int, estado_pago_data: dict) -> Optional[EstadoPago]:
        pass
    
    @abstractmethod
    async def delete(self, id_estado_pago: int) -> bool:
        pass
    
    @abstractmethod
    async def get_all(self) -> List[EstadoPago]:
        pass