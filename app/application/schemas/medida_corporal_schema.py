from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from zoneinfo import ZoneInfo

class MedidaCorporalBase(BaseModel):
    cuello: Optional[float] = None
    bicep_izquierdo: Optional[float] = None
    bicep_derecho: Optional[float] = None
    pecho: Optional[float] = None
    antebrazo_izquierdo: Optional[float] = None
    antebrazo_derecho: Optional[float] = None
    cintura: Optional[float] = None
    cadera: Optional[float] = None
    femoral_izquierdo: Optional[float] = None
    femoral_derecho: Optional[float] = None
    gemelo_izquierdo: Optional[float] = None
    gemelo_derecho: Optional[float] = None
    peso: Optional[float] = None
    altura: Optional[float] = None
    musculo: Optional[float] = None
    notas_adicionales: Optional[str] = Field(None, max_length=500)
    fecha_creacion: datetime = Field(
        default_factory=lambda: datetime.now(ZoneInfo("America/Guayaquil")),
        description="Fecha de creación con zona horaria Guayaquil"
    )

class MedidaCorporalUpdate(BaseModel):
    cuello: Optional[float] = None
    bicep_izquierdo: Optional[float] = None
    bicep_derecho: Optional[float] = None
    pecho: Optional[float] = None
    antebrazo_izquierdo: Optional[float] = None
    antebrazo_derecho: Optional[float] = None
    cintura: Optional[float] = None
    cadera: Optional[float] = None
    femoral_izquierdo: Optional[float] = None
    femoral_derecho: Optional[float] = None
    gemelo_izquierdo: Optional[float] = None
    gemelo_derecho: Optional[float] = None
    peso: Optional[float] = None
    altura: Optional[float] = None
    musculo: Optional[float] = None
    notas_adicionales: Optional[str] = Field(None, max_length=500)
    fecha_creacion: Optional[datetime] = None

class MedidaCorporalInDB(MedidaCorporalBase):
    id_medida_corporal: int
    id_cliente: int

    class Config:
        from_attributes = True

class MedidaCorporalResponse(MedidaCorporalInDB):
    pass
