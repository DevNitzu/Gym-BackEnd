from sqlalchemy import Column, Integer, String, Boolean,TIMESTAMP, func
from app.infrastructure.database.base import Base

class Empresa(Base):
    __tablename__ = "empresas"
    
    id_empresa = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    ruc = Column(String(100), nullable=False)
    direccion = Column(String(100), nullable=False)
    telefono = Column(String(100), nullable=False)
    correo = Column(String(100), nullable=False)
    activo = Column(Boolean, default=True)
    fecha_creacion = Column(TIMESTAMP, server_default=func.now(), nullable=False)