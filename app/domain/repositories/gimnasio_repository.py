from abc import ABC, abstractmethod
from app.domain.models.gimnasio import Gimnasio
from typing import Optional, List

class GimnasioRepository(ABC):
    @abstractmethod
    async def create(self, gimnasio: Gimnasio) -> Gimnasio:
        pass
    
    @abstractmethod
    async def get_by_id(self, id_gimnasio: int) -> Optional[Gimnasio]:
        pass
    
    @abstractmethod
    async def update(self, id_gimnasio: int, gimnasio_data: dict) -> Optional[Gimnasio]:
        pass
    
    @abstractmethod
    async def delete(self, id_gimnasio: int) -> bool:
        pass
    
    @abstractmethod
    async def get_all(self, id_empresa: int) -> List[Gimnasio]:
        pass