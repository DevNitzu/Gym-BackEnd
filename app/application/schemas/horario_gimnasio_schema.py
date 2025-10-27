from pydantic import BaseModel, Field
from typing import Optional
from datetime import time

class HorarioGimnasioBase(BaseModel):
    id_gimnasio: int = Field(..., description="ID del gimnasio")
    dia_semana: int = Field(..., ge=0, le=6, description="0=lunes, 6=domingo")
    hora_apertura: time = Field(..., description="Hora de apertura")
    hora_cierre: time = Field(..., description="Hora de cierre")

class HorarioGimnasioUpdate(BaseModel):
    id_gimnasio: Optional[int] = None
    dia_semana: Optional[int] = Field(None, ge=0, le=6, description="0=domingo, 6=sábado")
    hora_apertura: Optional[time] = None
    hora_cierre: Optional[time] = None

class HorarioGimnasioInDB(HorarioGimnasioBase):
    id_horario_gimnasio: int
    activo: bool

    class Config:
        from_attributes = True

class HorarioGimnasioResponse(HorarioGimnasioInDB):
    pass
