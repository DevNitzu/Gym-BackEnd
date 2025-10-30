from sqlalchemy import Column, Integer, Numeric, String, TIMESTAMP, Time, ForeignKey,Boolean, func
from app.core.base import Base

class Membresia(Base):
    __tablename__ = "membresias"
    
    id_membresia = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_gimnasio = Column(Integer, ForeignKey("gimnasios.id_gimnasio"), nullable=False)
    id_cliente = Column(Integer, ForeignKey("cliente.id_cliente"), nullable=False)
    id_metodo_pago = Column(Integer, ForeignKey("metodo_pago.id_metodo_pago"), nullable=False)
    id_estado_pago = Column(Integer, ForeignKey("estado_pago.id_estado_pago"), nullable=False)
    
    unidad_duracion = Column(String(15), nullable=False, comment="Unidad de duración: dia, mes, año")
    cantidad_duracion = Column(Integer, nullable=False, comment="Número de unidades de duración (ej. 3 meses, 10 días)")

    precio_unitario = Column(Numeric(10,2), nullable=False)
    descuento = Column(Numeric(1,2), default=0)
    precio_total = Column(Numeric(10,2), nullable=False)

    fecha_creacion = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    fecha_inicio = Column(Time, nullable=False)
    fecha_expiracion = Column(Time, nullable=False)
    renovable = Column(Boolean, default=True) # si la asistencia es flexible o no
    activo = Column(Boolean, default=True) # si ya no esta activa la membresia
