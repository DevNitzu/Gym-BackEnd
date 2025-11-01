from pydantic import BaseModel
from typing import Optional, List
from app.application.schemas.empleado_schema import EmpleadoInDB

class AsignacionDetalle(BaseModel):
    id_empresa: Optional[int] = None
    nombre_empresa: Optional[str] = None
    id_gimnasio: Optional[int] = None
    nombre_gimnasio: Optional[str] = None
    id_tipo_empleado: Optional[int] = None
    tipo_empleado_nombre: Optional[str] = None
    activo: Optional[bool] = True

class EmpleadoDTO(BaseModel):
    empleado: EmpleadoInDB
    asignaciones: List[AsignacionDetalle] = []

class EmpleadoAsignacionInfoResponse(BaseModel):
    data: List[EmpleadoDTO]
