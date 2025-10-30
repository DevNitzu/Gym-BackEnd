from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime
from datetime import datetime
from zoneinfo import ZoneInfo

class ClienteBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100)
    apellido: str = Field(..., min_length=2, max_length=100)
    cedula: str = Field(..., min_length=5, max_length=20)
    correo: EmailStr
    telefono: str = Field(..., min_length=7, max_length=15)
    fecha_creacion: datetime = Field(
        default_factory=lambda: datetime.now(ZoneInfo("America/Guayaquil")),
        description="Fecha de creación con zona horaria Guayaquil"
    )

class ClienteCreate(ClienteBase):
    contrasena: str = Field(..., min_length=6, max_length=100)

class ClienteUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=2, max_length=100)
    apellido: Optional[str] = Field(None, min_length=2, max_length=100)
    cedula: Optional[str] = Field(None, min_length=5, max_length=20)
    correo: Optional[EmailStr] = None
    telefono: Optional[str] = Field(..., min_length=7, max_length=15)
    contrasena: Optional[str] = Field(None, min_length=6, max_length=100)
    fecha_creacion: Optional[datetime] = None

class ClienteInDB(ClienteBase):
    id_cliente: int
    activo: bool

    class Config:
        from_attributes = True

class ClienteResponse(ClienteInDB):
    pass

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    correo: Optional[str] = None

class LoginRequest(BaseModel):
    correo: EmailStr
    contrasena: str