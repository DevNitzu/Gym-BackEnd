from abc import ABC, abstractmethod
from app.domain.models.empresa import Empresa
from typing import Optional, List

class EmpresaRepository(ABC):
    @abstractmethod
    async def create(self, empresa: Empresa) -> Empresa:
        pass
    
    @abstractmethod
    async def get_by_id(self, id_empresa: int) -> Optional[Empresa]:
        pass
    
    @abstractmethod
    async def update(self, id_empresa: int, empresa_data: dict) -> Optional[Empresa]:
        pass
    
    @abstractmethod
    async def delete(self, id_empresa: int) -> bool:
        pass
    
    @abstractmethod
    async def get_all(self) -> List[Empresa]:
        pass