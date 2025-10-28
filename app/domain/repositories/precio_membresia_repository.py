from abc import ABC, abstractmethod
from app.domain.models.precio_membresia import PrecioMembresia
from typing import Optional, List

class PrecioMembresiaRepository(ABC):
    @abstractmethod
    async def create(self, precio_membresia: PrecioMembresia) -> PrecioMembresia:
        pass
    
    @abstractmethod
    async def get_by_id(self, id_precio_membresia: int) -> Optional[PrecioMembresia]:
        pass
    
    @abstractmethod
    async def update(self, id_precio_membresia: int, precio_membresia_data: dict) -> Optional[PrecioMembresia]:
        pass
    
    @abstractmethod
    async def delete(self, id_precio_membresia: int) -> bool:
        pass
    
    @abstractmethod
    async def get_all(self, id_empresa: int) -> List[PrecioMembresia]:
        pass