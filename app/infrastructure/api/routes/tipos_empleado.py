from fastapi import APIRouter, Depends, HTTPException, status, Request
from app.application.services.tipo_empleado_service import TipoEmpleadoService
from app.infrastructure.database.repositories.tipo_empleado_repository_impl import TipoEmpleadoRepositoryImpl
from app.infrastructure.database.base import get_db
from app.application.schemas.tipo_empleado_schema import TipoEmpleadoBase, TipoEmpleadoUpdate, TipoEmpleadoResponse
from app.core.decorators import public_endpoint, private_endpoint
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

# Dependencia del servicio
def get_tipo_empleado_service(db: AsyncSession = Depends(get_db)) -> TipoEmpleadoService:
    tipo_empleado_repository = TipoEmpleadoRepositoryImpl(db)
    return TipoEmpleadoService(tipo_empleado_repository)

# Crear módulo
@router.post("/tipo_empleados", response_model=TipoEmpleadoResponse)
@public_endpoint
async def create_tipo_empleado(
    request: Request,
    tipo_empleado_data: TipoEmpleadoBase,
    tipo_empleado_service: TipoEmpleadoService = Depends(get_tipo_empleado_service)
):
    try:
        return await tipo_empleado_service.create_tipo_empleado(tipo_empleado_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Obtener todos los módulos
@router.get("/tipo_empleados", response_model=List[TipoEmpleadoResponse])
@public_endpoint
async def get_all_tipo_empleados(
    request: Request,
    tipo_empleado_service: TipoEmpleadoService = Depends(get_tipo_empleado_service)
):
    return await tipo_empleado_service.get_all_tipo_empleados()

# Obtener módulo por ID
@router.get("/tipo_empleados/{id_tipo_empleado}", response_model=TipoEmpleadoResponse)
@public_endpoint
async def get_tipo_empleado(
    request: Request,
    id_tipo_empleado: int,
    tipo_empleado_service: TipoEmpleadoService = Depends(get_tipo_empleado_service)
):
    tipo_empleado = await tipo_empleado_service.get_tipo_empleado(id_tipo_empleado)
    if not tipo_empleado:
        raise HTTPException(status_code=404, detail="Tipo Empleado no encontrado")
    return tipo_empleado

# Actualizar módulo
@router.put("/tipo_empleados/{id_tipo_empleado}", response_model=TipoEmpleadoResponse)
@public_endpoint
async def update_tipo_empleado(
    request: Request,
    id_tipo_empleado: int,
    tipo_empleado_data: TipoEmpleadoUpdate,
    tipo_empleado_service: TipoEmpleadoService = Depends(get_tipo_empleado_service)
):
    try:
        tipo_empleado = await tipo_empleado_service.update_tipo_empleado(id_tipo_empleado, tipo_empleado_data)
        if not tipo_empleado:
            raise HTTPException(status_code=404, detail="Tipo Empleado no encontrado")
        return tipo_empleado
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Eliminar módulo (soft delete)
@router.delete("/tipo_empleados/{id_tipo_empleado}")
@public_endpoint
async def delete_tipo_empleado(
    request: Request,
    id_tipo_empleado: int,
    tipo_empleado_service: TipoEmpleadoService = Depends(get_tipo_empleado_service)
):
    success = await tipo_empleado_service.delete_tipo_empleado(id_tipo_empleado)
    if not success:
        raise HTTPException(status_code=404, detail="Tipo Empleado no encontrado")
    return {"message": "Tipo Empleado eliminado exitosamente"}
