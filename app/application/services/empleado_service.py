from app.domain.repositories.empleado_repository import EmpleadoRepository
from app.application.schemas.empleado_schema import EmpleadoCreate, EmpleadoUpdate, EmpleadoInDB, LoginRequest
from app.core.security import get_password_hash, verify_password, create_access_token
from datetime import timedelta
from app.core.config import settings
from typing import Optional, List

class EmpleadoService:
    def __init__(self, empleado_repository: EmpleadoRepository):
        self.empleado_repository = empleado_repository

    # ----------------------
    # CREAR EMPLEADO
    # ----------------------
    async def create_empleado(self, empleado_data: EmpleadoCreate) -> EmpleadoInDB:
        # Validaciones
        existing_email = await self.empleado_repository.get_by_correo(empleado_data.correo)
        if existing_email:
            raise ValueError("El correo proporcionado ya está registrado")

        existing_cedula = await self.empleado_repository.get_by_cedula(empleado_data.cedula)
        if existing_cedula:
            raise ValueError("La cédula proporcionada ya está registrada")

        # Hashear contraseña
        empleado_dict = empleado_data.model_dump()
        empleado_dict["contrasena"] = get_password_hash(empleado_data.contrasena)

        # Crear en DB
        empleado_db = await self.empleado_repository.create(empleado_dict)

        # Devolver Pydantic validado
        return EmpleadoInDB.model_validate(empleado_db)

    # ----------------------
    # AUTENTICACIÓN
    # ----------------------
    async def authenticate_empleado(self, login_data: LoginRequest) -> dict:
        empleado = await self.empleado_repository.get_by_correo(login_data.correo)
        if not empleado or not verify_password(login_data.contrasena, empleado.contrasena):
            raise ValueError("Credenciales inválidas")

        if not empleado.activo:
            raise ValueError("Cuenta inhabilitada")

        access_token = create_access_token(
            data={"sub": empleado.correo},
            expires_delta=timedelta(minutes=settings.access_token_expire_minutes)
        )

        return {"access_token": access_token, "token_type": "bearer"}

    # ----------------------
    # ACTUALIZAR EMPLEADO
    # ----------------------
    async def update_empleado(self, id_empleado: int, empleado_data: EmpleadoUpdate) -> Optional[EmpleadoInDB]:
        update_dict = empleado_data.model_dump(exclude_unset=True)

        # Si se está actualizando la contraseña, hashearla
        if "contrasena" in update_dict:
            password_hash = get_password_hash(update_dict["contrasena"])
            empleado_password = await self.empleado_repository.get_by_id(id_empleado)
            if empleado_password and verify_password(update_dict["contrasena"], empleado_password.contrasena):
                raise ValueError("La nueva contraseña no puede ser igual a la anterior")
            update_dict["contrasena"] = password_hash

        empleado_db = await self.empleado_repository.update(id_empleado, update_dict)
        if not empleado_db:
            return None

        return EmpleadoInDB.model_validate(empleado_db)

    # ----------------------
    # ELIMINAR EMPLEADO
    # ----------------------
    async def delete_empleado(self, id_empleado: int) -> bool:
        return await self.empleado_repository.delete(id_empleado)

    # ----------------------
    # OBTENER EMPLEADO POR ID
    # ----------------------
    async def get_empleado(self, id_empleado: int) -> Optional[EmpleadoInDB]:
        empleado_db = await self.empleado_repository.get_by_id(id_empleado)
        if not empleado_db:
            return None
        return EmpleadoInDB.model_validate(empleado_db)

    # ----------------------
    # OBTENER TODOS LOS EMPLEADOS
    # ----------------------
    async def get_all_empleados(self) -> List[EmpleadoInDB]:
        empleados_db = await self.empleado_repository.get_all()
        return [EmpleadoInDB.model_validate(emp) for emp in empleados_db]
