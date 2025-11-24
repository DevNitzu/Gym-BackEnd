from app.domain.repositories.cliente_repository import ClienteRepository
from app.application.schemas.cliente_schema import ClienteCreate, ClienteUpdate, ClienteInDB, LoginRequest
from app.core.security import get_password_hash, verify_password, create_access_token
from datetime import timedelta
from app.core.config import settings
from typing import Optional, List

class ClienteService:
    def __init__(self, cliente_repository: ClienteRepository):
        self.cliente_repository = cliente_repository

    # ----------------------
    # CREAR EMPLEADO
    # ----------------------
    async def create_cliente(self, cliente_data: ClienteCreate) -> ClienteInDB:
        # Validaciones
        existing_email = await self.cliente_repository.get_by_correo(cliente_data.correo)
        if existing_email:
            raise ValueError("El correo proporcionado ya está registrado")

        existing_cedula = await self.cliente_repository.get_by_cedula(cliente_data.cedula)
        if existing_cedula:
            raise ValueError("La cédula proporcionada ya está registrada")

        # Hashear contraseña
        cliente_dict = cliente_data.model_dump()
        cliente_dict["contrasena"] = get_password_hash(cliente_data.contrasena)

        # Crear en DB
        cliente_db = await self.cliente_repository.create(cliente_dict)

        # Devolver Pydantic validado
        return ClienteInDB.model_validate(cliente_db)

    # ----------------------
    # AUTENTICACIÓN
    # ----------------------
    async def authenticate_cliente(self, login_data: LoginRequest) -> dict:
        cliente = await self.cliente_repository.get_by_correo(login_data.correo)
        if not cliente or not verify_password(login_data.contrasena, cliente.contrasena):
            raise ValueError("Credenciales inválidas")

        if not cliente.activo:
            raise ValueError("Cuenta inhabilitada")

        access_token = create_access_token(user_id=cliente.id_cliente,user_type="cliente")
        

        return {"access_token": access_token, "token_type": "bearer"}

    # ----------------------
    # ACTUALIZAR EMPLEADO
    # ----------------------
    async def update_cliente(self, id_cliente: int, cliente_data: ClienteUpdate) -> Optional[ClienteInDB]:
        update_dict = cliente_data.model_dump(exclude_unset=True)

        # Si se está actualizando la contraseña, hashearla
        if "contrasena" in update_dict:
            update_dict["contrasena"] = get_password_hash(update_dict["contrasena"])

        cliente_db = await self.cliente_repository.update(id_cliente, update_dict)
        if not cliente_db:
            return None

        return ClienteInDB.model_validate(cliente_db)

    # ----------------------
    # ELIMINAR EMPLEADO
    # ----------------------
    async def delete_cliente(self, id_cliente: int) -> bool:
        return await self.cliente_repository.delete(id_cliente)

    # ----------------------
    # OBTENER EMPLEADO POR ID
    # ----------------------
    async def get_cliente(self, id_cliente: int) -> Optional[ClienteInDB]:
        cliente_db = await self.cliente_repository.get_by_id(id_cliente)
        if not cliente_db:
            return None
        return ClienteInDB.model_validate(cliente_db)

    # ----------------------
    # OBTENER TODOS LOS EMPLEADOS
    # ----------------------
    async def get_all_clientes(self) -> List[ClienteInDB]:
        clientes_db = await self.cliente_repository.get_all()
        return [ClienteInDB.model_validate(emp) for emp in clientes_db]
