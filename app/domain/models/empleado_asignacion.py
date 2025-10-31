from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey, func
from app.core.base import Base

class EmpleadoAsignacion(Base):
    __tablename__ = "empleados_asignacion"
    
    id_empleado_asignacion = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_empresa = Column(Integer, ForeignKey("empresas.id_empresa"), nullable=True)
    id_gimnasio = Column(Integer, ForeignKey("gimnasios.id_gimnasio"), nullable=True)
    id_empleado = Column(Integer, ForeignKey("empleados.id_empleado"), nullable=True)
    id_tipo_empleado = Column(Integer, ForeignKey("tipos_empleado.id_tipo_empleado"), nullable=True)
    activo = Column(Boolean, default=True)
    fecha_asignacion = Column(TIMESTAMP, server_default=func.now(), nullable=False)
