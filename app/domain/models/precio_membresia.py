from sqlalchemy import Column, Integer, Numeric, String, TIMESTAMP, ForeignKey,Boolean, func
from app.core.base import Base

class PrecioMembresia(Base):
    __tablename__ = "precios_membresia"
    
    id_precio_membresia = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_gimnasio = Column(Integer, ForeignKey("gimnasios.id_gimnasio"), nullable=False)
    tipo = Column(String(10), nullable=False)
    precio = Column(Numeric(10,2), nullable=False)
    fecha_creacion = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    activo = Column(Boolean, default=True)
