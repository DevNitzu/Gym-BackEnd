from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey, func
from app.core.base import Base

class Cliente(Base):
    __tablename__ = "clientes"
    
    id_cliente = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    cedula = Column(String(100), nullable=False)
    correo = Column(String(100), nullable=False)
    contrasena = Column(String(100), nullable=False)
    telefono = Column(String(100), nullable=False)
    activo = Column(Boolean, default=True)
    genero = Column(Boolean, default=True) # True para masculino, False para femenino
    fecha_nacimiento = Column(TIMESTAMP, nullable=True)
    fecha_creacion = Column(TIMESTAMP, server_default=func.now(), nullable=False)
