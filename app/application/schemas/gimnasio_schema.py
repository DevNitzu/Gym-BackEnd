from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Optional
from datetime import datetime

class GimnasioBase(BaseModel):
    id_empresa: int = Field(..., description="ID de la empresa dueña del gimnasio")
    nombre: str = Field(..., min_length=2, max_length=100)
    direccion: str = Field(..., min_length=2, max_length=200)
    telefono: str = Field(..., min_length=7, max_length=15)
    correo: EmailStr = Field(...)
    activo: bool = Field(default=True)
    fecha_creacion: datetime = Field(default_factory=datetime.utcnow)

    # Validaciones Pydantic V2
    @field_validator("telefono")
    @classmethod
    def check_telefono(cls, v):
        if not v.isdigit():
            raise ValueError("El teléfono debe contener solo números")
        return v


class GimnasioUpdate(BaseModel):
    id_empresa: Optional[int] = None
    nombre: Optional[str] = Field(None, min_length=2, max_length=100)
    direccion: Optional[str] = Field(None, min_length=2, max_length=200)
    telefono: Optional[str] = Field(None, min_length=7, max_length=15)
    correo: Optional[EmailStr] = None
    activo: Optional[bool] = None
    fecha_creacion: Optional[datetime] = None

    @field_validator("telefono")
    @classmethod
    def check_telefono(cls, v):
        if v and not v.isdigit():
            raise ValueError("El teléfono debe contener solo números")
        return v


class GimnasioInDB(GimnasioBase):
    id_gimnasio: int

    class Config:
        from_attributes = True


class GimnasioResponse(GimnasioInDB):
    pass
