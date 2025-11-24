from fastapi import APIRouter, Depends, HTTPException, status, Request, UploadFile, File
from app.application.services.asistencia_service import AsistenciaService
from app.infrastructure.database.repositories.asistencia_repository_impl import AsistenciaRepositoryImpl
from app.core.base import get_db
from app.application.schemas.asistencia_schema import AsistenciaBase, AsistenciaUpdate, AsistenciaResponse
from app.core.decorators import auth_required,user_type_required
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

# Dependencia del servicio
def get_asistencia_service(db: AsyncSession = Depends(get_db)) -> AsistenciaService:
    asistencia_repository = AsistenciaRepositoryImpl(db)
    return AsistenciaService(asistencia_repository)

@router.post("/asistencias", response_model=AsistenciaResponse)
@auth_required
@user_type_required("empleado")
async def create_asistencia(
    request: Request,
    asistencia_data: AsistenciaBase,
    asistencia_service: AsistenciaService = Depends(get_asistencia_service)
):
    try:
        return await asistencia_service.create_asistencia(asistencia_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/asistencias", response_model=List[AsistenciaResponse])
@auth_required
@user_type_required("empleado")
async def get_all_asistencias(
    request: Request,
    asistencia_service: AsistenciaService = Depends(get_asistencia_service)
):
    return await asistencia_service.get_all_asistencias()

@router.get("/asistencias/{id_asistencia}", response_model=AsistenciaResponse)
@auth_required
@user_type_required("empleado")
async def get_asistencia(
    request: Request,
    id_asistencia: int,
    asistencia_service: AsistenciaService = Depends(get_asistencia_service)
):
    asistencia = await asistencia_service.get_asistencia(id_asistencia)
    if not asistencia:
        raise HTTPException(status_code=404, detail="Asistencia no encontrado")
    return asistencia

@router.put("/asistencias/{id_asistencia}", response_model=AsistenciaResponse)
@auth_required
@user_type_required("empleado")
async def update_asistencia(
    request: Request,
    id_asistencia: int,
    asistencia_data: AsistenciaUpdate,
    asistencia_service: AsistenciaService = Depends(get_asistencia_service)
):
    try:
        asistencia = await asistencia_service.update_asistencia(id_asistencia, asistencia_data)
        if not asistencia:
            raise HTTPException(status_code=404, detail="Asistencia no encontrado")
        return asistencia
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/asistencias/{id_asistencia}")
@auth_required
@user_type_required("empleado")
async def delete_asistencia(
    request: Request,
    id_asistencia: int,
    asistencia_service: AsistenciaService = Depends(get_asistencia_service)
):
    success = await asistencia_service.delete_asistencia(id_asistencia)
    if not success:
        raise HTTPException(status_code=404, detail="Asistencia no encontrado")
    return {"message": "Asistencia eliminada exitosamente"}

@router.put("/asistencias/logo/{id_asistencia}", response_model=AsistenciaResponse)
@auth_required
@user_type_required("empleado")
async def update_asistencia_logo(
    id_asistencia: int,
    logo_file: UploadFile = File(...),
    asistencia_service: AsistenciaService = Depends(get_asistencia_service)
):
    asistencia = await asistencia_service.update_asistencia_logo(id_asistencia, logo_file)
    if not asistencia:
        raise HTTPException(status_code=404, detail="Asistencia no encontrada")
    return asistencia