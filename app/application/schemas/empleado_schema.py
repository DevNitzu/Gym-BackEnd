from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime

class EmpleadoBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100)
    apellido: str = Field(..., min_length=2, max_length=100)
    cedula: str = Field(..., min_length=5, max_length=20)
    correo: EmailStr
    id_empresa: int
    id_gimnasio: Optional[int] = None
    id_tipo_empleado: Optional[int] = None
    fecha_creacion: datetime = Field(default_factory=datetime.utcnow)

class EmpleadoCreate(EmpleadoBase):
    contrasena: str = Field(..., min_length=6, max_length=100)

class EmpleadoUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=2, max_length=100)
    apellido: Optional[str] = Field(None, min_length=2, max_length=100)
    cedula: Optional[str] = Field(None, min_length=5, max_length=20)
    correo: Optional[EmailStr] = None
    id_empresa: Optional[int] = None
    id_gimnasio: Optional[int] = None
    id_tipo_empleado: Optional[int] = None
    contrasena: Optional[str] = Field(None, min_length=6, max_length=100)
    activo: Optional[bool] = None
    fecha_creacion: Optional[datetime] = None

class EmpleadoInDB(EmpleadoBase):
    id_empleado: int
    activo: bool

    class Config:
        from_attributes = True

class EmpleadoResponse(EmpleadoInDB):
    pass

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    correo: Optional[str] = None

class LoginRequest(BaseModel):
    correo: EmailStr
    contrasena: str