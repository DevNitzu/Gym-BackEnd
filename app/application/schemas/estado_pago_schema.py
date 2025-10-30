from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime

class EstadoPagoBase(BaseModel):
    nombre: str = Field(..., description="Nombre del estado de pago")

class EstadoPagoUpdate(BaseModel):
    nombre: Optional[str] = None

class EstadoPagoInDB(EstadoPagoBase):
    id_estado_pago: int
    activo: bool

    class Config:
        from_attributes = True

class EstadoPagoResponse(EstadoPagoInDB):
    pass
