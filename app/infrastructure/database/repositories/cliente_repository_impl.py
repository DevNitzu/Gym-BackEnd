from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.domain.models.cliente import Cliente
from typing import Optional, List
from app.domain.repositories.cliente_repository import ClienteRepository

class ClienteRepositoryImpl(ClienteRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, cliente_data: dict) -> Cliente:
        db_cliente = Cliente(**cliente_data)
        self.db.add(db_cliente)
        await self.db.commit()
        await self.db.refresh(db_cliente)
        return db_cliente

    async def get_by_id(self, id_cliente: int) -> Optional[Cliente]:
        result = await self.db.execute(
            select(Cliente).where(Cliente.id_cliente == id_cliente, Cliente.activo == True)
        )
        return result.scalar_one_or_none()

    async def update(self, id_cliente: int, cliente_data: dict) -> Optional[Cliente]:
        cliente = await self.get_by_id(id_cliente)
        if not cliente:
            return None
        for key, value in cliente_data.items():
            setattr(cliente, key, value)
        await self.db.commit()
        await self.db.refresh(cliente)
        return cliente

    async def delete(self, id_cliente: int) -> bool:
        cliente = await self.get_by_id(id_cliente)
        if not cliente:
            return False
        cliente.activo = False
        await self.db.commit()
        return True

    async def get_all(self) -> List[Cliente]:
        result = await self.db.execute(
            select(Cliente).where(Cliente.activo == True)
        )
        return result.scalars().all()
    
    async def get_by_correo(self, correo: str) -> Optional[Cliente]:
        query = select(Cliente).where(Cliente.correo == correo)
        result = await self.db.execute(query)
        cliente = result.scalars().first()
        return cliente

    async def get_by_cedula(self, cedula: str) -> Optional[Cliente]:
        query = select(Cliente).where(Cliente.cedula == cedula)
        result = await self.db.execute(query)
        cliente = result.scalars().first()
        return cliente
