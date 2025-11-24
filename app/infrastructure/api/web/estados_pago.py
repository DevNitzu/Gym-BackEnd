from fastapi import APIRouter, Depends, HTTPException, status, Request
from app.application.services.estado_pago_service import EstadoPagoService
from app.infrastructure.database.repositories.estado_pago_repository_impl import EstadoPagoRepositoryImpl
from app.core.base import get_db
from app.application.schemas.estado_pago_schema import EstadoPagoBase, EstadoPagoUpdate, EstadoPagoResponse
from app.core.decorators import auth_required, user_type_required
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

# Dependencia del servicio
def get_estado_pago_service(db: AsyncSession = Depends(get_db)) -> EstadoPagoService:
    estado_pago_repository = EstadoPagoRepositoryImpl(db)
    return EstadoPagoService(estado_pago_repository)

@router.post("/estado_pagos", response_model=EstadoPagoResponse)
@auth_required
@user_type_required("empleado")
async def create_estado_pago(
    request: Request,
    estado_pago_data: EstadoPagoBase,
    estado_pago_service: EstadoPagoService = Depends(get_estado_pago_service)
):
    try:
        return await estado_pago_service.create_estado_pago(estado_pago_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/estado_pagos", response_model=List[EstadoPagoResponse])
@auth_required
@user_type_required("empleado")
async def get_all_estado_pagos(
    request: Request,
    estado_pago_service: EstadoPagoService = Depends(get_estado_pago_service)
):
    return await estado_pago_service.get_all_estado_pagos()

@router.get("/estado_pagos/{id_estado_pago}", response_model=EstadoPagoResponse)
@auth_required
@user_type_required("empleado")
async def get_estado_pago(
    request: Request,
    id_estado_pago: int,
    estado_pago_service: EstadoPagoService = Depends(get_estado_pago_service)
):
    estado_pago = await estado_pago_service.get_estado_pago(id_estado_pago)
    if not estado_pago:
        raise HTTPException(status_code=404, detail="EstadoPago no encontrado")
    return estado_pago

@router.put("/estado_pagos/{id_estado_pago}", response_model=EstadoPagoResponse)
@auth_required
@user_type_required("empleado")
async def update_estado_pago(
    request: Request,
    id_estado_pago: int,
    estado_pago_data: EstadoPagoUpdate,
    estado_pago_service: EstadoPagoService = Depends(get_estado_pago_service)
):
    try:
        estado_pago = await estado_pago_service.update_estado_pago(id_estado_pago, estado_pago_data)
        if not estado_pago:
            raise HTTPException(status_code=404, detail="EstadoPago no encontrado")
        return estado_pago
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/estado_pagos/{id_estado_pago}")
@auth_required
@user_type_required("empleado")
async def delete_estado_pago(
    request: Request,
    id_estado_pago: int,
    estado_pago_service: EstadoPagoService = Depends(get_estado_pago_service)
):
    success = await estado_pago_service.delete_estado_pago(id_estado_pago)
    if not success:
        raise HTTPException(status_code=404, detail="EstadoPago no encontrado")
    return {"message": "EstadoPago eliminada exitosamente"}
