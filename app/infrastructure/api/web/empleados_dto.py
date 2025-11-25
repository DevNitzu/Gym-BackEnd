from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.application.dto.empleado_dto_schema import EmpleadoDTO, EmpleadoAsignacionInfoResponse
from app.application.services.empleado_dto_services import EmpleadoDTOService
from app.infrastructure.database.repositories.empleado_repository_impl import EmpleadoRepositoryImpl
from app.infrastructure.database.repositories.empleado_asignacion_repository_impl import EmpleadoAsignacionRepositoryImpl
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.base import get_db
from app.core.decorators import auth_required, user_type_required

router = APIRouter()

def get_empleado_info_service(db: AsyncSession = Depends(get_db)) -> EmpleadoDTOService:
    empleado_repo = EmpleadoRepositoryImpl(db)
    asignacion_repo = EmpleadoAsignacionRepositoryImpl(db)
    return EmpleadoDTOService(empleado_repo, asignacion_repo)


@router.get("/empleadodto/empresa/{id_empresa}", response_model=EmpleadoAsignacionInfoResponse)
@auth_required
@user_type_required("empleado")
async def get_empleados_por_empresa(
    request: Request,
    id_empresa: int,
    service: EmpleadoDTOService = Depends(get_empleado_info_service)
):
    empleados = await service.get_empleados_by_empresa(id_empresa)
    return {"data": empleados}


@router.get("/empleadodto/gimnasio/{id_gimnasio}", response_model=EmpleadoAsignacionInfoResponse)
@auth_required
@user_type_required("empleado")
async def get_empleados_por_gimnasio(
    request: Request,
    id_gimnasio: int,
    service: EmpleadoDTOService = Depends(get_empleado_info_service)
):
    empleados = await service.get_empleados_by_gimnasio(id_gimnasio)
    return {"data": empleados}


@router.get("/empleadodto/empleado/{id_empleado}", response_model=EmpleadoDTO)
@auth_required
@user_type_required("empleado")
async def get_empleado_info(
    request: Request,
    id_empleado: int,
    service: EmpleadoDTOService = Depends(get_empleado_info_service)
):
    empleado_info = await service.get_empleado_info(id_empleado)
    if not empleado_info:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    return empleado_info
