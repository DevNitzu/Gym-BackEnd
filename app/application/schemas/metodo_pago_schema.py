from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime

class MetodoPagoBase(BaseModel):
    nombre: str = Field(..., description="Nombre del metodo de pago")

class MetodoPagoUpdate(BaseModel):
    nombre: Optional[str] = None

class MetodoPagoInDB(MetodoPagoBase):
    id_metodo_pago: int
    activo: bool

    class Config:
        from_attributes = True

class MetodoPagoResponse(MetodoPagoInDB):
    pass
