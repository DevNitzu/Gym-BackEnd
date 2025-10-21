from abc import ABC, abstractmethod
from app.domain.models.modulo import Modulo
from typing import Optional, List

class ModuloRepository(ABC):
    @abstractmethod
    async def create(self, modulo: Modulo) -> Modulo:
        pass
    
    @abstractmethod
    async def get_by_id(self, id_modulo: int) -> Optional[Modulo]:
        pass
    
    @abstractmethod
    async def update(self, id_modulo: int, modulo_data: dict) -> Optional[Modulo]:
        pass
    
    @abstractmethod
    async def delete(self, id_modulo: int) -> bool:
        pass
    
    @abstractmethod
    async def get_all(self) -> List[Modulo]:
        pass