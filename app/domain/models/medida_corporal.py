from sqlalchemy import Column, Integer,Boolean, ForeignKey, func, TIMESTAMP, String, Float
from app.core.base import Base

class MedidaCorporal(Base):
    __tablename__ = "medidas_corporales"
    
    id_medida_corporal = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_cliente = Column(Integer, ForeignKey("clientes.id_cliente"), nullable=False)
    cuello = Column(Float, nullable=True)
    bicep_izquierdo = Column(Float, nullable=True)
    bicep_derecho = Column(Float, nullable=True)
    pecho = Column(Float, nullable=True)
    antebrazo_izquierdo = Column(Float, nullable=True)
    antebrazo_derecho = Column(Float, nullable=True)
    cintura = Column(Float, nullable=True)
    cadera = Column(Float, nullable=True)
    femoral_izquierdo = Column(Float, nullable=True)
    femoral_derecho = Column(Float, nullable=True)
    gemelo_izquierdo = Column(Float, nullable=True)
    gemelo_derecho = Column(Float, nullable=True)
    peso = Column(Float, nullable=True)
    altura = Column(Float, nullable=True)
    musculo = Column(Float, nullable=True)
    notas_adicionales = Column(String(500), nullable=True)
    activo = Column(Boolean, default=True)
    fecha_creacion = Column(TIMESTAMP, server_default=func.now(), nullable=False)