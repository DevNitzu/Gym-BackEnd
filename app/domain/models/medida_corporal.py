from sqlalchemy import Column, Integer,Boolean, ForeignKey, func, TIMESTAMP, String
from app.core.base import Base

class MedidaCorporal(Base):
    __tablename__ = "medidas_corporales"
    
    id_medida_corporal = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_cliente = Column(Integer, ForeignKey("clientes.id_cliente"), nullable=False)
    cuello = Column(float, nullable=True)
    bicep_izquierdo = Column(float, nullable=True)
    bicep_derecho = Column(float, nullable=True)
    pecho = Column(float, nullable=True)
    antebrazo_izquierdo = Column(float, nullable=True)
    antebrazo_derecho = Column(float, nullable=True)
    cintura = Column(float, nullable=True)
    cadera = Column(float, nullable=True)
    femoral_izquierdo = Column(float, nullable=True)
    femoral_derecho = Column(float, nullable=True)
    gemelo_izquierdo = Column(float, nullable=True)
    gemelo_derecho = Column(float, nullable=True)
    peso = Column(float, nullable=True)
    altura = Column(float, nullable=True)
    musculo = Column(float, nullable=True)
    notas_adicionales = Column(String(500), nullable=True)
    activo = Column(Boolean, default=True)
    fecha_creacion = Column(TIMESTAMP, server_default=func.now(), nullable=False)