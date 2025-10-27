from app.domain.repositories.empresa_repository import EmpresaRepository
from app.application.schemas.empresa_schema import EmpresaBase, EmpresaUpdate, EmpresaInDB
from typing import Optional, List

class EmpresaService:
    def __init__(self, empresa_repository: EmpresaRepository):
        self.empresa_repository = empresa_repository

    async def create_empresa(self, empresa_data: EmpresaBase) -> EmpresaInDB:
        existing_ruc = await self.empresa_repository.get_by_ruc(empresa_data.ruc)
        if existing_ruc:
            raise ValueError("El RUC proporcionado ya está registrado")
        
        empresa_dict = empresa_data.model_dump()
        empresa_db = await self.empresa_repository.create(empresa_dict)

        return EmpresaInDB.model_validate(empresa_db)

    async def update_empresa(self, id_empresa: int, empresa_data: EmpresaUpdate) -> Optional[EmpresaInDB]:
        existing_ruc = await self.empresa_repository.get_by_ruc(empresa_data.ruc)
        if existing_ruc and existing_ruc.id_empresa != id_empresa:
            raise ValueError("El RUC proporcionado ya está registrado")

        updated_db = await self.empresa_repository.update(
            id_empresa,
            empresa_data.model_dump(exclude_unset=True),
        )
        if not updated_db:
            return None
        return EmpresaInDB.model_validate(updated_db)


    async def delete_empresa(self, id_empresa: int) -> bool:
        return await self.empresa_repository.delete(id_empresa)

    async def get_empresa(self, id_empresa: int) -> Optional[EmpresaInDB]:
        empresa_db = await self.empresa_repository.get_by_id(id_empresa)
        if not empresa_db:
            return None
        return EmpresaInDB.model_validate(empresa_db)

    async def get_all_empresas(self) -> List[EmpresaInDB]:
        empresas_db = await self.empresa_repository.get_all()
        return [EmpresaInDB.model_validate(m) for m in empresas_db]