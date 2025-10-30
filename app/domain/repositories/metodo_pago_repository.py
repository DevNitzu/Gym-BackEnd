from abc import ABC, abstractmethod
from app.domain.models.metodo_pago import MetodoPago
from typing import Optional, List

class MetodoPagoRepository(ABC):
    @abstractmethod
    async def create(self, metodo_pago: MetodoPago) -> MetodoPago:
        pass
    
    @abstractmethod
    async def get_by_id(self, id_metodo_pago: int) -> Optional[MetodoPago]:
        pass
    
    @abstractmethod
    async def update(self, id_metodo_pago: int, metodo_pago_data: dict) -> Optional[MetodoPago]:
        pass
    
    @abstractmethod
    async def delete(self, id_metodo_pago: int) -> bool:
        pass
    
    @abstractmethod
    async def get_all(self) -> List[MetodoPago]:
        pass