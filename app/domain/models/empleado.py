from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey, func
from app.core.base import Base

class Empleado(Base):
    __tablename__ = "empleados"
    
    id_empleado = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_empresa = Column(Integer, ForeignKey("empresas.id_empresa"), nullable=False)
    id_gimnasio = Column(Integer, ForeignKey("gimnasios.id_gimnasio"), nullable=True)
    id_tipo_empleado = Column(Integer, ForeignKey("tipos_empleado.id_tipo"), nullable=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    cedula = Column(String(100), nullable=False)
    correo = Column(String(100), nullable=False)
    contrasena = Column(String(100), nullable=False)
    telefono = Column(String(100), nullable=False)
    activo = Column(Boolean, default=True)
    fecha_creacion = Column(TIMESTAMP, server_default=func.now(), nullable=False)
