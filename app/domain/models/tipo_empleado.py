from sqlalchemy import Column, Integer, String, Boolean
from app.infrastructure.database.base import Base

class TipoEmpleado(Base):
    __tablename__ = "tipos_empleado"
    
    id_tipo = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String(100), nullable=False)
    activo = Column(Boolean, default=True)