from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey, func
from app.core.base import Base

class EstadoPago(Base):
    __tablename__ = "estados_pago"
    
    id_estado_pago = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    activo = Column(Boolean, default=True)
