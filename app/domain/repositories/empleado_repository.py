from abc import ABC, abstractmethod
from app.domain.models.empleado import Empleado
from typing import Optional, List

class EmpleadoRepository(ABC):
    @abstractmethod
    async def create(self, empleado: Empleado) -> Empleado:
        pass
    
    @abstractmethod
    async def get_by_id(self, id_empleado: int) -> Optional[Empleado]:
        pass
    
    @abstractmethod
    async def update(self, id_empleado: int, empleado_data: dict) -> Optional[Empleado]:
        pass
    
    @abstractmethod
    async def delete(self, id_empleado: int) -> bool:
        pass
    
    @abstractmethod
    async def get_all(self) -> List[Empleado]:
        pass

    @abstractmethod
    async def get_by_correo(self, email: str) -> Optional[Empleado]:
        pass
    
    @abstractmethod
    async def get_by_cedula(self, cedula: str) -> Optional[Empleado]:
        pass