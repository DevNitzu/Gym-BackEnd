from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Optional
from datetime import datetime

class EmpresaBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100)
    ruc: str = Field(..., min_length=10, max_length=13)
    direccion: str = Field(..., min_length=2, max_length=200)
    telefono: str = Field(..., min_length=7, max_length=20)
    correo: EmailStr = Field(...)
    fecha_creacion: datetime = Field(default_factory=datetime.utcnow)
    activo: bool = Field(default=True)

    @field_validator("ruc")
    @classmethod
    def check_ruc_length(cls, v):
        if not (10 <= len(v) <= 13):
            raise ValueError("El RUC debe tener entre 10 y 13 dígitos")
        return v

    @field_validator("telefono")
    @classmethod
    def check_telefono(cls, v):
        if not v.isdigit():
            raise ValueError("El teléfono debe contener solo números")
        return v


class EmpresaUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=2, max_length=100)
    ruc: Optional[str] = Field(None, min_length=10, max_length=13)
    direccion: Optional[str] = Field(None, min_length=2, max_length=200)
    telefono: Optional[str] = Field(None, min_length=7, max_length=15)
    correo: Optional[EmailStr] = None
    fecha_creacion: Optional[datetime] = None
    activo: Optional[bool] = None

    @field_validator("ruc")
    @classmethod
    def check_ruc_length(cls, v):
        if v and not (10 <= len(v) <= 13):
            raise ValueError("El RUC debe tener entre 10 y 13 dígitos")
        return v

    @field_validator("telefono")
    @classmethod
    def check_telefono(cls, v):
        if v and not v.isdigit():
            raise ValueError("El teléfono debe contener solo números")
        return v


class EmpresaInDB(EmpresaBase):
    id_empresa: int
    logo_url: Optional[str] = None
    
    class Config:
        from_attributes = True


class EmpresaResponse(EmpresaInDB):
    pass


