from fastapi import APIRouter, Depends, HTTPException, status, Request
from app.application.services.medida_corporal_service import MedidaCorporalService
from app.infrastructure.database.repositories.medida_corporal_repository_impl import MedidaCorporalRepositoryImpl
from app.core.base import get_db
from app.application.schemas.medida_corporal_schema import MedidaCorporalBase, MedidaCorporalUpdate, MedidaCorporalResponse
from app.core.decorators import public_endpoint, private_endpoint
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

# Dependencia del servicio
def get_medida_corporal_service(db: AsyncSession = Depends(get_db)) -> MedidaCorporalService:
    medida_corporal_repository = MedidaCorporalRepositoryImpl(db)
    return MedidaCorporalService(medida_corporal_repository)

@router.post("/medidas_corporales", response_model=MedidaCorporalResponse)
@public_endpoint
async def create_medida_corporal(
    request: Request,
    medida_corporal_data: MedidaCorporalBase,
    medida_corporal_service: MedidaCorporalService = Depends(get_medida_corporal_service)
):
    try:
        return await medida_corporal_service.create_medida_corporal(medida_corporal_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/medidas_corporales/", response_model=List[MedidaCorporalResponse])
@public_endpoint
async def get_all_medidas_corporales(
    request: Request,
    id_empresa: int,
    medida_corporal_service: MedidaCorporalService = Depends(get_medida_corporal_service)
):
    return await medida_corporal_service.get_all_medida_corporals(id_empresa)

@router.get("/medidas_corporales/{id_medida_corporal}", response_model=MedidaCorporalResponse)
@public_endpoint
async def get_medida_corporal(
    request: Request,
    id_medida_corporal: int,
    medida_corporal_service: MedidaCorporalService = Depends(get_medida_corporal_service)
):
    medida_corporal = await medida_corporal_service.get_medida_corporal(id_medida_corporal)
    if not medida_corporal:
        raise HTTPException(status_code=404, detail="MedidaCorporal no encontrado")
    return medida_corporal

@router.put("/medidas_corporales/{id_medida_corporal}", response_model=MedidaCorporalResponse)
@public_endpoint
async def update_medida_corporal(
    request: Request,
    id_medida_corporal: int,
    medida_corporal_data: MedidaCorporalUpdate,
    medida_corporal_service: MedidaCorporalService = Depends(get_medida_corporal_service)
):
    try:
        medida_corporal = await medida_corporal_service.update_medida_corporal(id_medida_corporal, medida_corporal_data)
        if not medida_corporal:
            raise HTTPException(status_code=404, detail="MedidaCorporal no encontrado")
        return medida_corporal
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/medidas_corporales/{id_medida_corporal}")
@public_endpoint
async def delete_medida_corporal(
    request: Request,
    id_medida_corporal: int,
    medida_corporal_service: MedidaCorporalService = Depends(get_medida_corporal_service)
):
    success = await medida_corporal_service.delete_medida_corporal(id_medida_corporal)
    if not success:
        raise HTTPException(status_code=404, detail="MedidaCorporal no encontrado")
    return {"message": "MedidaCorporal eliminada exitosamente"}


@router.get("/medidas_corporales/historico/cliente/{id_cliente}", response_model=List[MedidaCorporalResponse])
@public_endpoint
async def get_all_medidas_corporales_by_cliente(
    request: Request,
    id_cliente: int,
    medida_corporal_service: MedidaCorporalService = Depends(get_medida_corporal_service)
):
    return await medida_corporal_service.get_all_medidas_coporales_by_cliente(id_cliente)

@router.get("/medidas_corporales/cliente/{id_cliente}", response_model=List[MedidaCorporalResponse])
@public_endpoint
async def get_last_medida_corporal_by_cliente(
    request: Request,
    id_cliente: int,
    medida_corporal_service: MedidaCorporalService = Depends(get_medida_corporal_service)
):
    return await medida_corporal_service.get_last_medida_coporal_by_cliente(id_cliente)