from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.database.base import get_db
from app.application.services.empleado_service import EmpleadoService
from app.infrastructure.database.repositories.empleado_repository_impl import EmpleadoRepositoryImpl
from app.application.schemas.empleado_schema import (
    EmpleadoCreate, EmpleadoUpdate, EmpleadoResponse, LoginRequest, Token
)
from app.core.decorators import public_endpoint, private_endpoint
from typing import List

router = APIRouter()

def get_empleado_service(db: AsyncSession = Depends(get_db)) -> EmpleadoService:
    empleado_repository = EmpleadoRepositoryImpl(db)
    return EmpleadoService(empleado_repository)

@router.post("/empleados/auth", response_model=Token)
@public_endpoint
async def login(
    request: Request,
    login_data: LoginRequest,
    empleado_service: EmpleadoService = Depends(get_empleado_service)
):
    try:
        return await empleado_service.authenticate_empleado(login_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/empleados", response_model=EmpleadoResponse)
@public_endpoint
async def create_empleado(
    request: Request,
    empleado_data: EmpleadoCreate,
    empleado_service: EmpleadoService = Depends(get_empleado_service)
):
    try:
        return await empleado_service.create_empleado(empleado_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/empleados", response_model=List[EmpleadoResponse])
@private_endpoint
async def get_all_empleados(
    request: Request,
    empleado_service: EmpleadoService = Depends(get_empleado_service)
):
    return await empleado_service.get_all_empleados()

@router.get("/empleados/{id_empleado}", response_model=EmpleadoResponse)
@private_endpoint
async def get_empleado(
    request: Request,
    id_empleado: int,
    empleado_service: EmpleadoService = Depends(get_empleado_service)
):
    empleado = await empleado_service.get_empleado(id_empleado)
    if not empleado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    return empleado

@router.put("/empleados/{id_empleado}", response_model=EmpleadoResponse)
@private_endpoint
async def update_empleado(
    request: Request,
    id_empleado: int,
    empleado_data: EmpleadoUpdate,
    empleado_service: EmpleadoService = Depends(get_empleado_service)
):
    empleado = await empleado_service.update_empleado(id_empleado, empleado_data)
    if not empleado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    return empleado

@router.delete("/empleados/{id_empleado}")
@private_endpoint
async def delete_empleado(
    request: Request,
    id_empleado: int,
    empleado_service: EmpleadoService = Depends(get_empleado_service)
):
    success = await empleado_service.delete_empleado(id_empleado)
    if not success:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    return {"message": "Empleado eliminado exitosamente"}