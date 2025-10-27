from abc import ABC, abstractmethod
from app.domain.models.horario_gimnasio import HorarioGimnasio
from typing import Optional, List

class HorarioGimnasioRepository(ABC):
    @abstractmethod
    async def create(self, horarioGimnasio: HorarioGimnasio) -> HorarioGimnasio:
        pass
    
    @abstractmethod
    async def get_by_id(self, id_horarioGimnasio: int) -> Optional[HorarioGimnasio]:
        pass
    
    @abstractmethod
    async def update(self, id_horarioGimnasio: int, horarioGimnasio_data: dict) -> Optional[HorarioGimnasio]:
        pass
    
    @abstractmethod
    async def delete(self, id_horarioGimnasio: int) -> bool:
        pass
    
    @abstractmethod
    async def get_all(self, id_gimnasio: int) -> List[HorarioGimnasio]:
        pass