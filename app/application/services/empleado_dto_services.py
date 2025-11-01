from app.domain.repositories.empleado_repository import EmpleadoRepository
from app.domain.repositories.empleado_asignacion_repository import EmpleadoAsignacionRepository
from app.application.dto.empleado_dto_schema import EmpleadoDTO, AsignacionDetalle
from app.application.schemas.empleado_schema import EmpleadoInDB
from typing import List

class EmpleadoDTOService:
    def __init__(
        self,
        empleado_repository: EmpleadoRepository,
        empleado_asignacion_repository: EmpleadoAsignacionRepository,
    ):
        self.empleado_repository = empleado_repository
        self.empleado_asignacion_repository = empleado_asignacion_repository

    # -------------------------------------
    # Obtener empleados con asignaciones por empresa
    # -------------------------------------
    async def get_empleados_by_empresa(self, id_empresa: int) -> List[EmpleadoDTO]:
        asignaciones = await self.empleado_asignacion_repository.get_all_empleados_asignaciones_by_empresa(id_empresa)
        empleados_dict = {}

        for a in asignaciones:
            if a.id_empleado not in empleados_dict:
                empleado_db = await self.empleado_repository.get_by_id(a.id_empleado)
                if not empleado_db:
                    continue

                empleados_dict[a.id_empleado] = EmpleadoDTO(
                    empleado=EmpleadoInDB.model_validate(empleado_db),
                    asignaciones=[]
                )

            empleados_dict[a.id_empleado].asignaciones.append(
                AsignacionDetalle(
                    id_empresa=a.id_empresa,
                    nombre_empresa=a.nombre_empresa,
                    id_gimnasio=a.id_gimnasio,
                    nombre_gimnasio=a.nombre_gimnasio,
                    id_tipo_empleado=a.id_tipo_empleado,
                    tipo_empleado_nombre=a.tipo_empleado_nombre,
                    activo=a.activo,
                )
            )

        return list(empleados_dict.values())

    # -------------------------------------
    # Obtener empleados de un gimnasio
    # -------------------------------------
    async def get_empleados_by_gimnasio(self, id_gimnasio: int) -> List[EmpleadoDTO]:
        asignaciones = await self.empleado_asignacion_repository.get_all_empleados_asignaciones_by_gimnasio(id_gimnasio)
        empleados_dict = {}

        for a in asignaciones:
            if a.id_empleado not in empleados_dict:
                empleado_db = await self.empleado_repository.get_by_id(a.id_empleado)
                if not empleado_db:
                    continue

                empleados_dict[a.id_empleado] = EmpleadoDTO(
                    empleado=EmpleadoInDB.model_validate(empleado_db),
                    asignaciones=[]
                )

            empleados_dict[a.id_empleado].asignaciones.append(
                AsignacionDetalle(
                    id_empresa=a.id_empresa,
                    nombre_empresa=a.nombre_empresa,
                    id_gimnasio=a.id_gimnasio,
                    nombre_gimnasio=a.nombre_gimnasio,
                    id_tipo_empleado=a.id_tipo_empleado,
                    tipo_empleado_nombre=a.tipo_empleado_nombre,
                    activo=a.activo,
                )
            )

        return list(empleados_dict.values())

    # -------------------------------------
    # Obtener información detallada de un solo empleado
    # -------------------------------------
    async def get_empleado_info(self, id_empleado: int) -> EmpleadoDTO:
        emp = await self.empleado_repository.get_by_id(id_empleado)
        if not emp:
            return None

        asignaciones = await self.empleado_asignacion_repository.get_empleado_asignacion_info(id_empleado)

        asignaciones_detalle = [
            AsignacionDetalle(
                id_empresa=a.id_empresa,
                nombre_empresa=a.nombre_empresa,
                id_gimnasio=a.id_gimnasio,
                nombre_gimnasio=a.nombre_gimnasio,
                id_tipo_empleado=a.id_tipo_empleado,
                tipo_empleado_nombre=a.tipo_empleado_nombre,
                activo=a.activo,
            )
            for a in asignaciones
        ]

        return EmpleadoDTO(
            empleado=EmpleadoInDB.model_validate(emp),
            asignaciones=asignaciones_detalle,
        )
