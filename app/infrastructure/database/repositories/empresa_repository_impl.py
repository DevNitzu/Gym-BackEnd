from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.domain.models.empresa import Empresa
from typing import Optional, List
from app.domain.repositories.empresa_repository import EmpresaRepository
from cloudinary.uploader import upload

class EmpresaRepositoryImpl(EmpresaRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, empresa_data: dict) -> Empresa:
        db_empresa = Empresa(**empresa_data)
        self.db.add(db_empresa)
        await self.db.commit()
        await self.db.refresh(db_empresa)
        return db_empresa

    async def get_by_id(self, id_empresa: int) -> Optional[Empresa]:
        result = await self.db.execute(
            select(Empresa).where(Empresa.id_empresa == id_empresa, Empresa.activo == True)
        )
        return result.scalar_one_or_none()

    async def update(self, id_empresa: int, empresa_data: dict, logo_file=None) -> Optional[Empresa]:
        empresa = await self.get_by_id(id_empresa)
        if not empresa:
            return None
        
        if logo_file:
            result = upload(logo_file.file, folder="empresas_logos")
            empresa_data["logo_url"] = result.get("secure_url")

        for key, value in empresa_data.items():
            setattr(empresa, key, value)

        await self.db.commit()
        await self.db.refresh(empresa)
        return empresa

    async def delete(self, id_empresa: int) -> bool:
        empresa = await self.get_by_id(id_empresa)
        if not empresa:
            return False
        empresa.activo = False
        await self.db.commit()
        return True

    async def get_all(self) -> List[Empresa]:
        result = await self.db.execute(
            select(Empresa).where(Empresa.activo == True)
        )
        return result.scalars().all()

    async def get_by_ruc(self, ruc: str) -> Optional[Empresa]:
        query = select(Empresa).where(Empresa.ruc == ruc)
        result = await self.db.execute(query)
        empresa = result.scalars().first()
        return empresa