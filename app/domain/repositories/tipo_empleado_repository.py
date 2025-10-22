from abc import ABC, abstractmethod
from app.domain.models.tipo_empleado import TipoEmpleado
from typing import Optional, List

class TipoEmpleadoRepository(ABC):
    @abstractmethod
    async def create(self, tipo_empleado: TipoEmpleado) -> TipoEmpleado:
        pass
    
    @abstractmethod
    async def get_by_id(self, id_tipo_empleado: int) -> Optional[TipoEmpleado]:
        pass
    
    @abstractmethod
    async def update(self, id_tipo_empleado: int, tipo_empleado_data: dict) -> Optional[TipoEmpleado]:
        pass
    
    @abstractmethod
    async def delete(self, id_tipo_empleado: int) -> bool:
        pass
    
    @abstractmethod
    async def get_all(self) -> List[TipoEmpleado]:
        pass