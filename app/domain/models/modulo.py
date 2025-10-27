from sqlalchemy import Column, Integer, String, Boolean
from app.core.base import Base

class Modulo(Base):
    __tablename__ = "modulos"
    
    id_modulo = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String(100), nullable=False)
    slug = Column(String(100), nullable=True)
    activo = Column(Boolean, default=True)