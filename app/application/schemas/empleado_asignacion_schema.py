from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime
from zoneinfo import ZoneInfo

class EmpleadoAsignacionBase(BaseModel):
    id_empresa: int = Field(..., description="ID de la empresa dueña del empleado_asignacion")
    id_gimnasio: int = Field(..., description="ID del empleado")
    id_empleado: int = Field(..., description="ID empleado")
    id_tipo_empleado: int = Field(..., description="ID del tipo empleado")
    fecha_asignacion: datetime = Field(
        default_factory=lambda: datetime.now(ZoneInfo("America/Guayaquil")),
        description="Fecha de creación con zona horaria Guayaquil"
    )

class EmpleadoAsignacionUpdate(BaseModel):
    id_empresa: Optional[int] = None
    id_gimnasio: Optional[int] = None
    id_empleado: Optional[int] = None
    id_tipo_empleado: Optional[int] = None

class EmpleadoAsignacionInDB(EmpleadoAsignacionBase):
    id_empleado_asignacion: int
    activo: bool
    pertenece_empresa: bool

    class Config:
        from_attributes = True


class EmpleadoAsignacionResponse(EmpleadoAsignacionInDB):
    pass
