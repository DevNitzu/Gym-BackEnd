from abc import ABC, abstractmethod
from app.domain.models.cliente import Cliente
from typing import Optional, List

class ClienteRepository(ABC):
    @abstractmethod
    async def create(self, cliente: Cliente) -> Cliente:
        pass
    
    @abstractmethod
    async def get_by_id(self, id_cliente: int) -> Optional[Cliente]:
        pass
    
    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[Cliente]:
        pass
    
    @abstractmethod
    async def get_by_cedula(self, cedula: str) -> Optional[Cliente]:
        pass
    
    @abstractmethod
    async def update(self, id_cliente: int, cliente_data: dict) -> Optional[Cliente]:
        pass
    
    @abstractmethod
    async def delete(self, id_cliente: int) -> bool:
        pass
    
    @abstractmethod
    async def get_all(self) -> List[Cliente]:
        pass