from pydantic import BaseModel, Field
from typing import Optional

class TipoEmpleadoBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100)
    descripcion: str = Field(..., min_length=2, max_length=100)

class TipoEmpleadoUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=2, max_length=100)
    descripcion: Optional[str] = Field(None, min_length=2, max_length=100)

class TipoEmpleadoInDB(TipoEmpleadoBase):
    id_tipo: int
    activo: bool

    class Config:
        from_attributes = True

class TipoEmpleadoResponse(TipoEmpleadoInDB):
    pass
