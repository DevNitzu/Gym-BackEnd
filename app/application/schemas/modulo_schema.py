from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ModuloBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100)
    descripcion: str = Field(..., min_length=2, max_length=100)
    slug: Optional[str] = Field(None, max_length=20)
    activo: bool = Field(...)

class ModuloUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=2, max_length=100)
    descripcion: Optional[str] = Field(None, min_length=2, max_length=100)
    slug: Optional[str] = Field(None, max_length=20)
    activo: Optional[bool] = Field(None)

class ModuloInDB(ModuloBase):
    id_modulo: int
    
    class Config:
        from_attributes = True

class ModuloResponse(ModuloInDB):
    pass
