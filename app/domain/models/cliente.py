from sqlalchemy import Column, Integer, String, Boolean
from app.infrastructure.database.base import Base

class Cliente(Base):
    __tablename__ = "clientes"
    
    id_cliente = Column(Integer, primary_key=True, index=True, autoincrement=True)
    cedula = Column(String(20), unique=True, index=True, nullable=False)
    nombres = Column(String(100), nullable=False)
    apellidos = Column(String(100), nullable=False)
    telefono = Column(String(20))
    email = Column(String(100), unique=True, index=True, nullable=False)
    direccion = Column(String(200))
    contrasenia = Column(String(255), nullable=False)
    estado = Column(Boolean, default=True)
    cantidad_personal = Column(Integer, default=0)