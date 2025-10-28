from fastapi import APIRouter, Depends, HTTPException, status, Request
from app.application.services.horario_gimnasio_service import HorarioGimnasioService
from app.infrastructure.database.repositories.horario_gimnasio_repository_impl import HorarioGimnasioRepositoryImpl
from app.core.base import get_db
from app.application.schemas.horario_gimnasio_schema import HorarioGimnasioBase, HorarioGimnasioUpdate, HorarioGimnasioResponse
from app.core.decorators import public_endpoint, private_endpoint
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

# Dependencia del servicio
def get_horario_gimnasio_service(db: AsyncSession = Depends(get_db)) -> HorarioGimnasioService:
    horario_gimnasio_repository = HorarioGimnasioRepositoryImpl(db)
    return HorarioGimnasioService(horario_gimnasio_repository)

@router.post("/horario_gimnasios", response_model=HorarioGimnasioResponse)
@public_endpoint
async def create_horario_gimnasio(
    request: Request,
    horario_gimnasio_data: HorarioGimnasioBase,
    horario_gimnasio_service: HorarioGimnasioService = Depends(get_horario_gimnasio_service)
):
    try:
        return await horario_gimnasio_service.create_horario_gimnasio(horario_gimnasio_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/horario_gimnasios/gimnasio/{id_gimnasio}", response_model=List[HorarioGimnasioResponse])
@public_endpoint
async def get_all_horario_gimnasios(
    request: Request,
    id_gimnasio: int,
    horario_gimnasio_service: HorarioGimnasioService = Depends(get_horario_gimnasio_service)
):
    return await horario_gimnasio_service.get_all_horario_gimnasios(id_gimnasio)

@router.get("/horario_gimnasios/{id_horario_gimnasio}", response_model=HorarioGimnasioResponse)
@public_endpoint
async def get_horario_gimnasio(
    request: Request,
    id_horario_gimnasio: int,
    horario_gimnasio_service: HorarioGimnasioService = Depends(get_horario_gimnasio_service)
):
    horario_gimnasio = await horario_gimnasio_service.get_horario_gimnasio(id_horario_gimnasio)
    if not horario_gimnasio:
        raise HTTPException(status_code=404, detail="HorarioGimnasio no encontrado")
    return horario_gimnasio

@router.put("/horario_gimnasios/{id_horario_gimnasio}", response_model=HorarioGimnasioResponse)
@public_endpoint
async def update_horario_gimnasio(
    request: Request,
    id_horario_gimnasio: int,
    horario_gimnasio_data: HorarioGimnasioUpdate,
    horario_gimnasio_service: HorarioGimnasioService = Depends(get_horario_gimnasio_service)
):
    try:
        horario_gimnasio = await horario_gimnasio_service.update_horario_gimnasio(id_horario_gimnasio, horario_gimnasio_data)
        if not horario_gimnasio:
            raise HTTPException(status_code=404, detail="HorarioGimnasio no encontrado")
        return horario_gimnasio
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/horario_gimnasios/{id_horario_gimnasio}")
@public_endpoint
async def delete_horario_gimnasio(
    request: Request,
    id_horario_gimnasio: int,
    horario_gimnasio_service: HorarioGimnasioService = Depends(get_horario_gimnasio_service)
):
    success = await horario_gimnasio_service.delete_horario_gimnasio(id_horario_gimnasio)
    if not success:
        raise HTTPException(status_code=404, detail="HorarioGimnasio no encontrado")
    return {"message": "HorarioGimnasio eliminada exitosamente"}
