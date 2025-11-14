from abc import ABC, abstractmethod
from app.domain.models.medida_corporal import MedidaCorporal
from typing import Optional, List

class MedidaCorporalRepository(ABC):
    @abstractmethod
    async def create(self, medida_corporal: MedidaCorporal) -> MedidaCorporal:
        pass
    
    @abstractmethod
    async def get_by_id(self, id_medida_corporal: int) -> Optional[MedidaCorporal]:
        pass
    
    @abstractmethod
    async def update(self, id_medida_corporal: int, medida_corporal_data: dict) -> Optional[MedidaCorporal]:
        pass
    
    @abstractmethod
    async def delete(self, id_medida_corporal: int) -> bool:
        pass
    
    @abstractmethod
    async def get_all(self) -> List[MedidaCorporal]:
        pass

    @abstractmethod
    async def get_all_by_cliente(self, id_cliente: int) -> Optional[MedidaCorporal]:
        pass
    
    @abstractmethod
    async def get_last_by_cliente(self, id_cliente: int) -> Optional[MedidaCorporal]:
        pass