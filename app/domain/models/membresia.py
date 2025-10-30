from sqlalchemy import Column, Integer, Numeric, String, TIMESTAMP, DateTime, ForeignKey, Boolean, func
from app.core.base import Base

class Membresia(Base):
    __tablename__ = "membresias"
    
    id_membresia = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_gimnasio = Column(Integer, ForeignKey("gimnasios.id_gimnasio"), nullable=False)
    id_cliente = Column(Integer, ForeignKey("clientes.id_cliente"), nullable=False)
    id_metodo_pago = Column(Integer, ForeignKey("metodos_pago.id_metodo_pago"), nullable=False)
    id_estado_pago = Column(Integer, ForeignKey("estados_pago.id_estado_pago"), nullable=False)
    
    unidad_duracion = Column(String(15), nullable=False, comment="Unidad de duración: dia, mes, año")
    cantidad_duracion = Column(Integer, nullable=False, comment="Número de unidades de duración (ej. 3 meses, 10 días)")

    precio_unitario = Column(Numeric(10,2), nullable=False)
    descuento = Column(Numeric(1,2), default=0)
    precio_total = Column(Numeric(10,2), nullable=False)

    fecha_creacion = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    fecha_inicio = Column(TIMESTAMP(timezone=True), nullable=False)
    fecha_expiracion = Column(TIMESTAMP(timezone=True), nullable=False)
    renovable = Column(Boolean, default=True)
    activo = Column(Boolean, default=True)
