from fastapi import APIRouter, Depends, HTTPException, status, Request
from app.application.services.membresia_service import MembresiaService
from app.infrastructure.database.repositories.membresia_repository_impl import MembresiaRepositoryImpl
from app.core.base import get_db
from app.application.schemas.membresia_schema import MembresiaBase, MembresiaUpdate, MembresiaResponse
from app.core.decorators import public_endpoint, private_endpoint
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

# Dependencia del servicio
def get_membresia_service(db: AsyncSession = Depends(get_db)) -> MembresiaService:
    membresia_repository = MembresiaRepositoryImpl(db)
    return MembresiaService(membresia_repository)

@router.post("/membresias", response_model=MembresiaResponse)
@public_endpoint
async def create_membresia(
    request: Request,
    membresia_data: MembresiaBase,
    membresia_service: MembresiaService = Depends(get_membresia_service)
):
    try:
        return await membresia_service.create_membresia(membresia_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/membresias/gimnasio/{id_gimnasio}", response_model=List[MembresiaResponse])
@public_endpoint
async def get_all_membresias(
    request: Request,
    id_gimnasio: int,
    membresia_service: MembresiaService = Depends(get_membresia_service)
):
    return await membresia_service.get_all_membresias(id_gimnasio)

@router.get("/membresias/{id_membresia}", response_model=MembresiaResponse)
@public_endpoint
async def get_membresia(
    request: Request,
    id_membresia: int,
    membresia_service: MembresiaService = Depends(get_membresia_service)
):
    membresia = await membresia_service.get_membresia(id_membresia)
    if not membresia:
        raise HTTPException(status_code=404, detail="Membresia no encontrado")
    return membresia

@router.put("/membresias/{id_membresia}", response_model=MembresiaResponse)
@public_endpoint
async def update_membresia(
    request: Request,
    id_membresia: int,
    membresia_data: MembresiaUpdate,
    membresia_service: MembresiaService = Depends(get_membresia_service)
):
    try:
        membresia = await membresia_service.update_membresia(id_membresia, membresia_data)
        if not membresia:
            raise HTTPException(status_code=404, detail="Membresia no encontrado")
        return membresia
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/membresias/{id_membresia}")
@public_endpoint
async def delete_membresia(
    request: Request,
    id_membresia: int,
    membresia_service: MembresiaService = Depends(get_membresia_service)
):
    success = await membresia_service.delete_membresia(id_membresia)
    if not success:
        raise HTTPException(status_code=404, detail="Membresia no encontrado")
    return {"message": "Membresia eliminada exitosamente"}

@router.get("/membresias/active_count/gimnasio/{id_gimnasio}")
@public_endpoint
async def get_count_active_membresias_by_gimnasio(
    request: Request,
    id_gimnasio: int,
    membresia_service: MembresiaService = Depends(get_membresia_service)
):
    count = await membresia_service.get_count_active_membresias_by_gimnasio(id_gimnasio)
    return {"active_membresias_count": count}

@router.get("/membresias/clientes_count/gimnasio/{id_gimnasio}")
@public_endpoint
async def get_count_clientes_membresia_by_gimnasio(
    request: Request,
    id_gimnasio: int,
    membresia_service: MembresiaService = Depends(get_membresia_service)
):
    count = await membresia_service.get_count_clientes_membresia_by_gimnasio(id_gimnasio)
    return {"clientes_membresia_count": count}