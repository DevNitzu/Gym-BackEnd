from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app.infrastructure.database.base import get_db
from app.application.services.cliente_service import ClienteService
from app.infrastructure.database.repositories.cliente_repository_impl import ClienteRepositoryImpl
from app.application.schemas.cliente_schema import (
    ClienteCreate, ClienteUpdate, ClienteResponse, LoginRequest, Token
)
from app.core.decorators import public_endpoint, private_endpoint
from typing import List

router = APIRouter()

def get_cliente_service(db: Session = Depends(get_db)) -> ClienteService:
    cliente_repository = ClienteRepositoryImpl(db)
    return ClienteService(cliente_repository)

@router.post("/clientes/auth", response_model=Token)
@public_endpoint
async def login(
    request: Request,
    login_data: LoginRequest,
    cliente_service: ClienteService = Depends(get_cliente_service)
):
    try:
        return await cliente_service.authenticate_cliente(login_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/clientes", response_model=ClienteResponse)
@public_endpoint
async def create_cliente(
    request: Request,
    cliente_data: ClienteCreate,
    cliente_service: ClienteService = Depends(get_cliente_service)
):
    try:
        return await cliente_service.create_cliente(cliente_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/clientes", response_model=List[ClienteResponse])
@private_endpoint
async def get_all_clientes(
    request: Request,
    cliente_service: ClienteService = Depends(get_cliente_service)
):
    return await cliente_service.get_all_clientes()

@router.get("/clientes/{id_cliente}", response_model=ClienteResponse)
@private_endpoint
async def get_cliente(
    request: Request,
    id_cliente: int,
    cliente_service: ClienteService = Depends(get_cliente_service)
):
    cliente = await cliente_service.get_cliente(id_cliente)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente

@router.put("/clientes/{id_cliente}", response_model=ClienteResponse)
@private_endpoint
async def update_cliente(
    request: Request,
    id_cliente: int,
    cliente_data: ClienteUpdate,
    cliente_service: ClienteService = Depends(get_cliente_service)
):
    cliente = await cliente_service.update_cliente(id_cliente, cliente_data)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encnontrado")
    return cliente

@router.delete("/clientes/{id_cliente}")
@private_endpoint
async def delete_cliente(
    request: Request,
    id_cliente: int,
    cliente_service: ClienteService = Depends(get_cliente_service)
):
    success = await cliente_service.delete_cliente(id_cliente)
    if not success:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return {"message": "Cliente eliminado exitosamente"}