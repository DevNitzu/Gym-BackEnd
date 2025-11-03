from abc import ABC, abstractmethod
from app.domain.models.asistencia import Asistencia
from typing import Optional, List

class AsistenciaRepository(ABC):
    @abstractmethod
    async def create(self, asistencia: Asistencia) -> Asistencia:
        pass
    
    @abstractmethod
    async def get_by_id(self, id_asistencia: int) -> Optional[Asistencia]:
        pass
    
    @abstractmethod
    async def update(self, id_asistencia: int, asistencia_data: dict) -> Optional[Asistencia]:
        pass
    
    @abstractmethod
    async def delete(self, id_asistencia: int) -> bool:
        pass
    
    @abstractmethod
    async def get_all(self) -> List[Asistencia]:
        pass