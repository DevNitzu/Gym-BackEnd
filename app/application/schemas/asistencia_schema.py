from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from zoneinfo import ZoneInfo

class AsistenciaBase(BaseModel):
    id_membresia: int = Field(..., description="ID de la membresía del cliente en el gimnasio")
    fecha_asistencia: datetime = Field(..., description="Fecha y hora de la asistencia")
    fecha_creacion: datetime = Field(
        default_factory=lambda: datetime.now(ZoneInfo("America/Guayaquil")),
        description="Fecha de creación con zona horaria Guayaquil"
    )

class AsistenciaUpdate(BaseModel):
    id_membresia: Optional[int] = None
    fecha_asistencia: Optional[datetime] = None

class AsistenciaInDB(AsistenciaBase):
    id_asistencia: int
    activo: bool

    class Config:
        from_attributes = True

class AsistenciaResponse(AsistenciaInDB):
    pass
