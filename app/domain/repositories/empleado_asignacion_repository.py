from abc import ABC, abstractmethod
from app.domain.models.empleado_asignacion import EmpleadoAsignacion
from typing import Optional, List

class EmpleadoAsignacionRepository(ABC):
    @abstractmethod
    async def create(self, empleado_asignacion: EmpleadoAsignacion) -> EmpleadoAsignacion:
        pass
    
    @abstractmethod
    async def get_by_id(self, id_empleado_asignacion: int) -> Optional[EmpleadoAsignacion]:
        pass
    
    @abstractmethod
    async def update(self, id_empleado_asignacion: int, empleado_asignacion_data: dict) -> Optional[EmpleadoAsignacion]:
        pass
    
    @abstractmethod
    async def delete(self, id_empleado_asignacion: int) -> bool:
        pass
    
    @abstractmethod
    async def get_all(self) -> List[EmpleadoAsignacion]:
        pass