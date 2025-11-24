from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.base import get_db
from app.application.services.cliente_service import ClienteService
from app.infrastructure.database.repositories.cliente_repository_impl import ClienteRepositoryImpl
from app.application.schemas.cliente_schema import (
    ClienteCreate, ClienteUpdate, ClienteResponse, LoginRequest, Token
)
from app.core.decorators import auth_required, user_type_required, public_endpoint
from typing import List

router = APIRouter()

def get_cliente_service(db: AsyncSession = Depends(get_db)) -> ClienteService:
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
async def create_cliente(
    request: Request,
    cliente_data: ClienteCreate,
    cliente_service: ClienteService = Depends(get_cliente_service)
):
    try:
        return await cliente_service.create_cliente(cliente_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/clientes/me", response_model=ClienteResponse)
@auth_required
@user_type_required("cliente")
async def update_cliente(
    request: Request,
    cliente_data: ClienteUpdate,
    cliente_service: ClienteService = Depends(get_cliente_service)
):
    id_cliente = int(request.state.user["sub"])    
    cliente = await cliente_service.update_cliente(id_cliente, cliente_data)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente

@router.get("/clientes/me", response_model=ClienteResponse)
@auth_required
@user_type_required("cliente")
async def get_me_cliente(
    request: Request,
    cliente_service: ClienteService = Depends(get_cliente_service)
):
    
    id_cliente = int(request.state.user["sub"])  
    return await cliente_service.get_cliente(id_cliente)
