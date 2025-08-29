from app.domain.repositories.cliente_repository import ClienteRepository
from app.application.schemas.cliente_schema import ClienteCreate, ClienteUpdate, LoginRequest
from app.core.security import get_password_hash, verify_password, create_access_token
from datetime import timedelta
from app.core.config import settings
from typing import Optional

class ClienteService:
    def __init__(self, cliente_repository: ClienteRepository):
        self.cliente_repository = cliente_repository

    async def create_cliente(self, cliente_data: ClienteCreate):
        existing_cliente = await self.cliente_repository.get_by_email(cliente_data.email)
        if existing_cliente:
            raise ValueError("El correo proporcionado ya está registrado")
        
        existing_cedula = await self.cliente_repository.get_by_cedula(cliente_data.cedula)
        if existing_cedula:
            raise ValueError("La cédula proporcionada ya está registrada")
        
        hashed_password = get_password_hash(cliente_data.contrasenia)
        
        cliente_dict = cliente_data.model_dump()
        cliente_dict["contrasenia"] = hashed_password
        
        return await self.cliente_repository.create(cliente_dict)

    async def authenticate_cliente(self, login_data: LoginRequest):
        cliente = await self.cliente_repository.get_by_email(login_data.email)
        if not cliente:
            raise ValueError("Invalid credentials")
        
        if not verify_password(login_data.contrasenia, cliente.contrasenia):
            raise ValueError("Invalid credentials password")

        if not cliente.estado:
            raise ValueError("Account is disabled")
        
        access_token = create_access_token(
            data={"sub": cliente.email},
            expires_delta=timedelta(minutes=settings.access_token_expire_minutes)
        )
        
        return {"access_token": access_token, "token_type": "bearer"}

    async def update_cliente(self, id_cliente: int, cliente_data: ClienteUpdate):
        return await self.cliente_repository.update(id_cliente, cliente_data.model_dump(exclude_unset=True))

    async def delete_cliente(self, id_cliente: int):
        return await self.cliente_repository.delete(id_cliente)

    async def get_cliente(self, id_cliente: int):
        return await self.cliente_repository.get_by_id(id_cliente)

    async def get_all_clientes(self):
        return await self.cliente_repository.get_all()