from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey, func
from app.core.base import Base

class Gimnasio(Base):
    __tablename__ = "gimnasios"
    
    id_gimnasio = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_empresa = Column(Integer, ForeignKey("empresas.id_empresa"), nullable=False)
    nombre = Column(String(100), nullable=False)
    direccion = Column(String(200), nullable=False)
    telefono = Column(String(15), nullable=False)
    correo = Column(String(100), nullable=False)
    activo = Column(Boolean, default=True)
    fecha_creacion = Column(TIMESTAMP, server_default=func.now(), nullable=False)
