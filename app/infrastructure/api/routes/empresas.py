from fastapi import APIRouter, Depends, HTTPException, status, Request
from app.application.services.empresa_service import EmpresaService
from app.infrastructure.database.repositories.empresa_repository_impl import EmpresaRepositoryImpl
from app.core.base import get_db
from app.application.schemas.empresa_schema import EmpresaBase, EmpresaUpdate, EmpresaResponse
from app.core.decorators import public_endpoint, private_endpoint
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

# Dependencia del servicio
def get_empresa_service(db: AsyncSession = Depends(get_db)) -> EmpresaService:
    empresa_repository = EmpresaRepositoryImpl(db)
    return EmpresaService(empresa_repository)

@router.post("/empresas", response_model=EmpresaResponse)
@public_endpoint
async def create_empresa(
    request: Request,
    empresa_data: EmpresaBase,
    empresa_service: EmpresaService = Depends(get_empresa_service)
):
    try:
        return await empresa_service.create_empresa(empresa_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/empresas", response_model=List[EmpresaResponse])
@public_endpoint
async def get_all_empresas(
    request: Request,
    empresa_service: EmpresaService = Depends(get_empresa_service)
):
    return await empresa_service.get_all_empresas()

@router.get("/empresas/{id_empresa}", response_model=EmpresaResponse)
@public_endpoint
async def get_empresa(
    request: Request,
    id_empresa: int,
    empresa_service: EmpresaService = Depends(get_empresa_service)
):
    empresa = await empresa_service.get_empresa(id_empresa)
    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa no encontrado")
    return empresa

@router.put("/empresas/{id_empresa}", response_model=EmpresaResponse)
@public_endpoint
async def update_empresa(
    request: Request,
    id_empresa: int,
    empresa_data: EmpresaUpdate,
    empresa_service: EmpresaService = Depends(get_empresa_service)
):
    try:
        empresa = await empresa_service.update_empresa(id_empresa, empresa_data)
        if not empresa:
            raise HTTPException(status_code=404, detail="Empresa no encontrado")
        return empresa
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/empresas/{id_empresa}")
@public_endpoint
async def delete_empresa(
    request: Request,
    id_empresa: int,
    empresa_service: EmpresaService = Depends(get_empresa_service)
):
    success = await empresa_service.delete_empresa(id_empresa)
    if not success:
        raise HTTPException(status_code=404, detail="Empresa no encontrado")
    return {"message": "Empresa eliminada exitosamente"}
