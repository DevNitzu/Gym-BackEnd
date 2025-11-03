from pydantic import BaseModel, Field, model_validator,field_validator
from typing import Optional
from datetime import datetime
from zoneinfo import ZoneInfo

class MembresiaBase(BaseModel):
    id_gimnasio: int = Field(..., description="ID del gimnasio")
    id_cliente: int = Field(..., description="ID del cliente")
    id_metodo_pago: int = Field(..., description="ID del método de pago")
    id_estado_pago: int = Field(..., description="ID del estado de pago")
    
    unidad_duracion: str = Field(..., description="Unidad de duración: 'dia', 'mes' o 'año'")
    cantidad_duracion: int = Field(..., gt=0, description="Número de unidades de duración (ej. 3 meses, 10 días)")
    
    precio_unitario: float = Field(..., gt=0, description="Precio unitario de la membresía")
    descuento: float = Field(0, ge=0, le=1, description="Descuento aplicado (ej. 0.15 = 15%)")
    precio_total: Optional[float] = Field(None, gt=0, description="Precio total de la membresía (calculado automáticamente)")
    
    fecha_creacion: datetime = Field(
        default_factory=lambda: datetime.now(ZoneInfo("America/Guayaquil")),
        description="Fecha de creación con zona horaria Guayaquil"
    )
    fecha_inicio: Optional[datetime] = Field(None, description="Fecha de inicio de la membresía")
    fecha_expiracion: Optional[datetime] = Field(None, description="Fecha de expiración de la membresía")
    
    renovable: bool = Field(True, description="Indica si la membresía es renovable")


    @field_validator("unidad_duracion")
    @classmethod
    def validar_unidad_duracion(cls, v: str) -> str:
        allowed = {"dia", "mes", "año"}
        if v not in allowed:
            raise ValueError(f"tipo debe ser uno de {allowed}")
        return v

class MembresiaUpdate(BaseModel):
    id_estado_pago: Optional[int] = Field(None, description="ID del nuevo estado de pago")
    renovable: Optional[bool] = Field(None, description="Indica si la membresía puede renovarse")

class MembresiaInDB(MembresiaBase):
    id_membresia: int
    activo: bool = Field(True, description="Indica si la membresía está activa")
    expirado: bool = Field(False, description="Indica si la membresía está activa")
    
    class Config:
        from_attributes = True


class MembresiaResponse(MembresiaInDB):
    pass
