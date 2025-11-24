from fastapi import APIRouter, Depends, HTTPException, status, Request
from app.application.services.gimnasio_service import GimnasioService
from app.infrastructure.database.repositories.gimnasio_repository_impl import GimnasioRepositoryImpl
from app.core.base import get_db
from app.application.schemas.gimnasio_schema import GimnasioBase, GimnasioUpdate, GimnasioResponse
from app.core.decorators import auth_required, user_type_required
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

# Dependencia del servicio
def get_gimnasio_service(db: AsyncSession = Depends(get_db)) -> GimnasioService:
    gimnasio_repository = GimnasioRepositoryImpl(db)
    return GimnasioService(gimnasio_repository)

@router.post("/gimnasios", response_model=GimnasioResponse)
@auth_required
@user_type_required("empleado")
async def create_gimnasio(
    request: Request,
    gimnasio_data: GimnasioBase,
    gimnasio_service: GimnasioService = Depends(get_gimnasio_service)
):
    try:
        return await gimnasio_service.create_gimnasio(gimnasio_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/gimnasios/{id_empresa}", response_model=List[GimnasioResponse])
@auth_required
@user_type_required("empleado")
async def get_all_gimnasios(
    request: Request,
    id_empresa: int,
    gimnasio_service: GimnasioService = Depends(get_gimnasio_service)
):
    return await gimnasio_service.get_all_gimnasios(id_empresa)

@router.get("/gimnasios/{id_gimnasio}", response_model=GimnasioResponse)
@auth_required
@user_type_required("empleado")
async def get_gimnasio(
    request: Request,
    id_gimnasio: int,
    gimnasio_service: GimnasioService = Depends(get_gimnasio_service)
):
    gimnasio = await gimnasio_service.get_gimnasio(id_gimnasio)
    if not gimnasio:
        raise HTTPException(status_code=404, detail="Gimnasio no encontrado")
    return gimnasio

@router.put("/gimnasios/{id_gimnasio}", response_model=GimnasioResponse)
@auth_required
@user_type_required("empleado")
async def update_gimnasio(
    request: Request,
    id_gimnasio: int,
    gimnasio_data: GimnasioUpdate,
    gimnasio_service: GimnasioService = Depends(get_gimnasio_service)
):
    try:
        gimnasio = await gimnasio_service.update_gimnasio(id_gimnasio, gimnasio_data)
        if not gimnasio:
            raise HTTPException(status_code=404, detail="Gimnasio no encontrado")
        return gimnasio
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/gimnasios/{id_gimnasio}")
@auth_required
@user_type_required("empleado")
async def delete_gimnasio(
    request: Request,
    id_gimnasio: int,
    gimnasio_service: GimnasioService = Depends(get_gimnasio_service)
):
    success = await gimnasio_service.delete_gimnasio(id_gimnasio)
    if not success:
        raise HTTPException(status_code=404, detail="Gimnasio no encontrado")
    return {"message": "Gimnasio eliminada exitosamente"}
