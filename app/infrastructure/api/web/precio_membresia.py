from fastapi import APIRouter, Depends, HTTPException, status, Request
from app.application.services.precio_membresia_service import PrecioMembresiaService
from app.infrastructure.database.repositories.precio_membresia_repository_impl import PrecioMembresiaRepositoryImpl
from app.core.base import get_db
from app.application.schemas.precio_membresia_schema import PrecioMembresiaBase, PrecioMembresiaUpdate, PrecioMembresiaResponse
from app.core.decorators import public_endpoint, private_endpoint
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

# Dependencia del servicio
def get_precio_membresia_service(db: AsyncSession = Depends(get_db)) -> PrecioMembresiaService:
    precio_membresia_repository = PrecioMembresiaRepositoryImpl(db)
    return PrecioMembresiaService(precio_membresia_repository)

@router.post("/precio_membresias", response_model=PrecioMembresiaResponse)
@public_endpoint
async def create_precio_membresia(
    request: Request,
    precio_membresia_data: PrecioMembresiaBase,
    precio_membresia_service: PrecioMembresiaService = Depends(get_precio_membresia_service)
):
    try:
        return await precio_membresia_service.create_precio_membresia(precio_membresia_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/precio_membresias/gimnasio/{id_gimnasio}", response_model=List[PrecioMembresiaResponse])
@public_endpoint
async def get_all_precio_membresias(
    request: Request,
    id_gimnasio: int,
    precio_membresia_service: PrecioMembresiaService = Depends(get_precio_membresia_service)
):
    return await precio_membresia_service.get_all_precio_membresias(id_gimnasio)

@router.get("/precio_membresias/{id_precio_membresia}", response_model=PrecioMembresiaResponse)
@public_endpoint
async def get_precio_membresia(
    request: Request,
    id_precio_membresia: int,
    precio_membresia_service: PrecioMembresiaService = Depends(get_precio_membresia_service)
):
    precio_membresia = await precio_membresia_service.get_precio_membresia(id_precio_membresia)
    if not precio_membresia:
        raise HTTPException(status_code=404, detail="PrecioMembresia no encontrado")
    return precio_membresia

@router.put("/precio_membresias/{id_precio_membresia}", response_model=PrecioMembresiaResponse)
@public_endpoint
async def update_precio_membresia(
    request: Request,
    id_precio_membresia: int,
    precio_membresia_data: PrecioMembresiaUpdate,
    precio_membresia_service: PrecioMembresiaService = Depends(get_precio_membresia_service)
):
    try:
        precio_membresia = await precio_membresia_service.update_precio_membresia(id_precio_membresia, precio_membresia_data)
        if not precio_membresia:
            raise HTTPException(status_code=404, detail="PrecioMembresia no encontrado")
        return precio_membresia
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/precio_membresias/{id_precio_membresia}")
@public_endpoint
async def delete_precio_membresia(
    request: Request,
    id_precio_membresia: int,
    precio_membresia_service: PrecioMembresiaService = Depends(get_precio_membresia_service)
):
    success = await precio_membresia_service.delete_precio_membresia(id_precio_membresia)
    if not success:
        raise HTTPException(status_code=404, detail="PrecioMembresia no encontrado")
    return {"message": "PrecioMembresia eliminada exitosamente"}
