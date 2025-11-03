from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, func
from app.core.base import Base

class Asistencia(Base):
    __tablename__ = "asistencias"
    
    id_asistencia = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_membresia = Column(Integer, ForeignKey("membresias.id_membresia"), nullable=False, index=True)
    fecha_asistencia = Column(DateTime, nullable=False, index=True)
    activo = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, server_default=func.now(), nullable=False)
