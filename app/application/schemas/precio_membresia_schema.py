from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime

class PrecioMembresiaBase(BaseModel):
    id_gimnasio: int = Field(..., description="ID del gimnasio")
    tipo: str = Field(..., description="Unidad de duración: dia, mes o año")
    precio: float = Field(..., gt=0, description="Precio del plan")
    fecha_creacion: datetime = Field(default_factory=datetime.utcnow)

    @field_validator("tipo")
    @classmethod
    def validar_tipo(cls, v: str) -> str:
        allowed = {"dia", "mes", "año"}
        if v not in allowed:
            raise ValueError(f"tipo debe ser uno de {allowed}")
        return v

class PrecioMembresiaUpdate(BaseModel):
    id_gimnasio: Optional[int] = None
    tipo: Optional[str] = None
    precio: Optional[float] = None
    fecha_creacion: Optional[datetime] = None

    @field_validator("tipo")
    @classmethod
    def validar_tipo(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        allowed = {"dia", "mes", "año"}
        if v not in allowed:
            raise ValueError(f"tipo debe ser uno de {allowed}")
        return v

class PrecioMembresiaInDB(PrecioMembresiaBase):
    id_precio_membresia: int
    activo: bool

    class Config:
        from_attributes = True

class PrecioMembresiaResponse(PrecioMembresiaInDB):
    pass
