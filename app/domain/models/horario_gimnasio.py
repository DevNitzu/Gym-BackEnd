from sqlalchemy import Column, Integer, String, Boolean,Time, ForeignKey, func
from app.core.base import Base

class HorarioGimnasio(Base):
    __tablename__ = "horarios_gimnasios"
    
    id_horario_gimnasio = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_gimnasio = Column(Integer, ForeignKey("empresas.id_empresa"), nullable=False)
    dia_semana= Column(Integer, nullable=False)
    hora_apertura = Column(Time, nullable=False)
    hora_cierre = Column(Time, nullable=False)
    activo = Column(Boolean, default=True)