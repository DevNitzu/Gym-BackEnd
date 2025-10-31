from fastapi import APIRouter, Depends, HTTPException, status, Request
from app.application.services.empleado_asignacion_service import EmpleadoAsignacionService
from app.infrastructure.database.repositories.empleado_asignacion_repository_impl import EmpleadoAsignacionRepositoryImpl
from app.core.base import get_db
from app.application.schemas.empleado_asignacion_schema import EmpleadoAsignacionBase, EmpleadoAsignacionUpdate, EmpleadoAsignacionResponse
from app.core.decorators import public_endpoint, private_endpoint
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

def get_empleado_asignacion_service(db: AsyncSession = Depends(get_db)) -> EmpleadoAsignacionService:
    empleado_asignacion_repository = EmpleadoAsignacionRepositoryImpl(db)
    return EmpleadoAsignacionService(empleado_asignacion_repository)

@router.post("/empleado_asignacions", response_model=EmpleadoAsignacionResponse)
@public_endpoint
async def create_empleado_asignacion(
    request: Request,
    empleado_asignacion_data: EmpleadoAsignacionBase,
    empleado_asignacion_service: EmpleadoAsignacionService = Depends(get_empleado_asignacion_service)
):
    try:
        return await empleado_asignacion_service.create_empleado_asignacion(empleado_asignacion_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/empleado_asignacions", response_model=List[EmpleadoAsignacionResponse])
@public_endpoint
async def get_all_empleados_asignacion(
    request: Request,
    empleado_asignacion_service: EmpleadoAsignacionService = Depends(get_empleado_asignacion_service)
):
    return await empleado_asignacion_service.get_all_empleados_asignacion()

@router.get("/empleado_asignacions/{id_empleado_asignacion}", response_model=EmpleadoAsignacionResponse)
@public_endpoint
async def get_empleado_asignacion(
    request: Request,
    id_empleado_asignacion: int,
    empleado_asignacion_service: EmpleadoAsignacionService = Depends(get_empleado_asignacion_service)
):
    empleado_asignacion = await empleado_asignacion_service.get_empleado_asignacion(id_empleado_asignacion)
    if not empleado_asignacion:
        raise HTTPException(status_code=404, detail="Tipo Empleado no encontrado")
    return empleado_asignacion

@router.put("/empleado_asignacions/{id_empleado_asignacion}", response_model=EmpleadoAsignacionResponse)
@public_endpoint
async def update_empleado_asignacion(
    request: Request,
    id_empleado_asignacion: int,
    empleado_asignacion_data: EmpleadoAsignacionUpdate,
    empleado_asignacion_service: EmpleadoAsignacionService = Depends(get_empleado_asignacion_service)
):
    try:
        empleado_asignacion = await empleado_asignacion_service.update_empleado_asignacion(id_empleado_asignacion, empleado_asignacion_data)
        if not empleado_asignacion:
            raise HTTPException(status_code=404, detail="Tipo Empleado no encontrado")
        return empleado_asignacion
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/empleado_asignacions/{id_empleado_asignacion}")
@public_endpoint
async def delete_empleado_asignacion(
    request: Request,
    id_empleado_asignacion: int,
    empleado_asignacion_service: EmpleadoAsignacionService = Depends(get_empleado_asignacion_service)
):
    success = await empleado_asignacion_service.delete_empleado_asignacion(id_empleado_asignacion)
    if not success:
        raise HTTPException(status_code=404, detail="Empleado asignacion no encontrado")
    return {"message": "Empleado asignacion eliminado exitosamente"}
