from fastapi import APIRouter, Depends, HTTPException, status, Request
from app.application.services.modulo_service import ModuloService
from app.infrastructure.database.repositories.modulo_repository_impl import ModuloRepositoryImpl
from app.core.base import get_db
from app.application.schemas.modulo_schema import ModuloBase, ModuloUpdate, ModuloResponse
from app.core.decorators import auth_required, user_type_required
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

# Dependencia del servicio
def get_modulo_service(db: AsyncSession = Depends(get_db)) -> ModuloService:
    modulo_repository = ModuloRepositoryImpl(db)
    return ModuloService(modulo_repository)

# Crear módulo
@router.post("/modulos", response_model=ModuloResponse)
@auth_required
@user_type_required("empleado")
async def create_modulo(
    request: Request,
    modulo_data: ModuloBase,
    modulo_service: ModuloService = Depends(get_modulo_service)
):
    try:
        return await modulo_service.create_modulo(modulo_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Obtener todos los módulos
@router.get("/modulos", response_model=List[ModuloResponse])
@auth_required
@user_type_required("empleado")
async def get_all_modulos(
    request: Request,
    modulo_service: ModuloService = Depends(get_modulo_service)
):
    return await modulo_service.get_all_modulos()

# Obtener módulo por ID
@router.get("/modulos/{id_modulo}", response_model=ModuloResponse)
@auth_required
@user_type_required("empleado")
async def get_modulo(
    request: Request,
    id_modulo: int,
    modulo_service: ModuloService = Depends(get_modulo_service)
):
    modulo = await modulo_service.get_modulo(id_modulo)
    if not modulo:
        raise HTTPException(status_code=404, detail="Módulo no encontrado")
    return modulo

# Actualizar módulo
@router.put("/modulos/{id_modulo}", response_model=ModuloResponse)
@auth_required
@user_type_required("empleado")
async def update_modulo(
    request: Request,
    id_modulo: int,
    modulo_data: ModuloUpdate,
    modulo_service: ModuloService = Depends(get_modulo_service)
):
    try:
        modulo = await modulo_service.update_modulo(id_modulo, modulo_data)
        if not modulo:
            raise HTTPException(status_code=404, detail="Módulo no encontrado")
        return modulo
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Eliminar módulo (soft delete)
@router.delete("/modulos/{id_modulo}")
@auth_required
@user_type_required("empleado")
async def delete_modulo(
    request: Request,
    id_modulo: int,
    modulo_service: ModuloService = Depends(get_modulo_service)
):
    success = await modulo_service.delete_modulo(id_modulo)
    if not success:
        raise HTTPException(status_code=404, detail="Módulo no encontrado")
    return {"message": "Módulo eliminado exitosamente"}
