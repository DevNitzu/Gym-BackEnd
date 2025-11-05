from abc import ABC, abstractmethod
from app.domain.models.membresia import Membresia
from typing import Optional, List

class MembresiaRepository(ABC):
    @abstractmethod
    async def create(self, horarioGimnasio: Membresia) -> Membresia:
        pass
    
    @abstractmethod
    async def get_by_id(self, id_horarioGimnasio: int) -> Optional[Membresia]:
        pass
    
    @abstractmethod
    async def update(self, id_horarioGimnasio: int, horarioGimnasio_data: dict) -> Optional[Membresia]:
        pass
    
    @abstractmethod
    async def delete(self, id_horarioGimnasio: int) -> bool:
        pass
    
    @abstractmethod
    async def get_all(self, id_gimnasio: int) -> List[Membresia]:
        pass

    @abstractmethod
    async def get_all(self, id_gimnasio: int) -> List[Membresia]:
        pass

    # Jobs

    @abstractmethod
    async def expire_membresias(self, current_date) -> int:
        pass
    
    # Report

    @abstractmethod
    async def get_count_active_membresias_by_gimnasio(self, id_gimnasio: int) -> int:
        pass

    @abstractmethod
    async def get_count_clientes_membresia_by_gimnasio(self, id_gimnasio: int) -> int:
        pass