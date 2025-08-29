from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime

class ClienteBase(BaseModel):
    cedula: str = Field(..., min_length=10, max_length=20)
    nombres: str = Field(..., min_length=2, max_length=100)
    apellidos: str = Field(..., min_length=2, max_length=100)
    telefono: Optional[str] = Field(None, max_length=20)
    email: EmailStr
    direccion: Optional[str] = Field(None, max_length=200)
    cantidad_personal: int = Field(0, ge=0)

class ClienteCreate(ClienteBase):
    contrasenia: str = Field(..., min_length=6)

class ClienteUpdate(BaseModel):
    nombres: Optional[str] = Field(None, min_length=2, max_length=100)
    apellidos: Optional[str] = Field(None, min_length=2, max_length=100)
    telefono: Optional[str] = Field(None, max_length=20)
    direccion: Optional[str] = Field(None, max_length=200)
    cantidad_personal: Optional[int] = Field(None, ge=0)

class ClienteInDB(ClienteBase):
    id_cliente: int
    estado: bool
    
    class Config:
        from_attributes = True

class ClienteResponse(ClienteInDB):
    pass

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class LoginRequest(BaseModel):
    email: EmailStr
    contrasenia: str