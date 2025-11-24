from fastapi import APIRouter, Depends, HTTPException, status, Request
from app.application.services.metodo_pago_service import MetodoPagoService
from app.infrastructure.database.repositories.metodo_pago_repository_impl import MetodoPagoRepositoryImpl
from app.core.base import get_db
from app.application.schemas.metodo_pago_schema import MetodoPagoBase, MetodoPagoUpdate, MetodoPagoResponse
from app.core.decorators import auth_required, user_type_required
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

# Dependencia del servicio
def get_metodo_pago_service(db: AsyncSession = Depends(get_db)) -> MetodoPagoService:
    metodo_pago_repository = MetodoPagoRepositoryImpl(db)
    return MetodoPagoService(metodo_pago_repository)

@router.post("/metodo_pagos", response_model=MetodoPagoResponse)
@auth_required
@user_type_required("empleado")
async def create_metodo_pago(
    request: Request,
    metodo_pago_data: MetodoPagoBase,
    metodo_pago_service: MetodoPagoService = Depends(get_metodo_pago_service)
):
    try:
        return await metodo_pago_service.create_metodo_pago(metodo_pago_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/metodo_pagos", response_model=List[MetodoPagoResponse])
@auth_required
@user_type_required("empleado")
async def get_all_metodo_pagos(
    request: Request,
    metodo_pago_service: MetodoPagoService = Depends(get_metodo_pago_service)
):
    return await metodo_pago_service.get_all_metodo_pagos()

@router.get("/metodo_pagos/{id_metodo_pago}", response_model=MetodoPagoResponse)
@auth_required
@user_type_required("empleado")
async def get_metodo_pago(
    request: Request,
    id_metodo_pago: int,
    metodo_pago_service: MetodoPagoService = Depends(get_metodo_pago_service)
):
    metodo_pago = await metodo_pago_service.get_metodo_pago(id_metodo_pago)
    if not metodo_pago:
        raise HTTPException(status_code=404, detail="MetodoPago no encontrado")
    return metodo_pago

@router.put("/metodo_pagos/{id_metodo_pago}", response_model=MetodoPagoResponse)
@auth_required
@user_type_required("empleado")
async def update_metodo_pago(
    request: Request,
    id_metodo_pago: int,
    metodo_pago_data: MetodoPagoUpdate,
    metodo_pago_service: MetodoPagoService = Depends(get_metodo_pago_service)
):
    try:
        metodo_pago = await metodo_pago_service.update_metodo_pago(id_metodo_pago, metodo_pago_data)
        if not metodo_pago:
            raise HTTPException(status_code=404, detail="MetodoPago no encontrado")
        return metodo_pago
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/metodo_pagos/{id_metodo_pago}")
@auth_required
@user_type_required("empleado")
async def delete_metodo_pago(
    request: Request,
    id_metodo_pago: int,
    metodo_pago_service: MetodoPagoService = Depends(get_metodo_pago_service)
):
    success = await metodo_pago_service.delete_metodo_pago(id_metodo_pago)
    if not success:
        raise HTTPException(status_code=404, detail="MetodoPago no encontrado")
    return {"message": "MetodoPago eliminada exitosamente"}
