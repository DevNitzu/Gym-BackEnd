# app/infrastructure/api/router.py
from fastapi import APIRouter

# =====================================================
#   IMPORTAR RUTAS – WEB
# =====================================================

from app.infrastructure.api.web import (
    clientes as clientes_web,
    modulos as modulos_web,
    empresas as empresas_web,
    gimnasios as gimnasios_web,
    tipos_empleado as tipos_empleado_web,
    empleados as empleados_web,
    horarios_gimnasio as horarios_gimnasio_web,
    precio_membresia as precio_membresia_web,
    estados_pago as estados_pago_web,
    metodo_pago as metodo_pago_web,
    membresias as membresias_web,
    empleados_asignacion as empleados_asignacion_web,
    asistencias as asistencias_web,
    empleados_dto as empleados_dto_web,
    medidas_corporales as medidas_corporales_web,
)

# =====================================================
#   IMPORTAR RUTAS – MÓVIL
# =====================================================

from app.infrastructure.api.app import clientes as clientes_movil

router = APIRouter()

# =====================================================
#                   WEB ROUTES
# =====================================================

router.include_router(
    clientes_web.router,
    prefix="/web/clientes",
    tags=["web_clientes"]
)

router.include_router(
    modulos_web.router,
    prefix="/web/modulos",
    tags=["web_modulos"]
)

router.include_router(
    empresas_web.router,
    prefix="/web/empresas",
    tags=["web_empresas"]
)

router.include_router(
    gimnasios_web.router,
    prefix="/web/gimnasios",
    tags=["web_gimnasios"]
)

router.include_router(
    tipos_empleado_web.router,
    prefix="/web/tipos_empleado",
    tags=["web_tipos_empleado"]
)

router.include_router(
    empleados_web.router,
    prefix="/web/empleados",
    tags=["web_empleados"]
)

router.include_router(
    horarios_gimnasio_web.router,
    prefix="/web/horarios_gimnasio",
    tags=["web_horarios_gimnasio"]
)

router.include_router(
    precio_membresia_web.router,
    prefix="/web/precio_membresia",
    tags=["web_precio_membresia"]
)

router.include_router(
    estados_pago_web.router,
    prefix="/web/estados_pago",
    tags=["web_estados_pago"]
)

router.include_router(
    metodo_pago_web.router,
    prefix="/web/metodo_pago",
    tags=["web_metodo_pago"]
)

router.include_router(
    membresias_web.router,
    prefix="/web/membresias",
    tags=["web_membresias"]
)

router.include_router(
    empleados_asignacion_web.router,
    prefix="/web/empleados_asignacion",
    tags=["web_empleados_asignacion"]
)

router.include_router(
    asistencias_web.router,
    prefix="/web/asistencias",
    tags=["web_asistencias"]
)

router.include_router(
    medidas_corporales_web.router,
    prefix="/web/medidas_corporales",
    tags=["web_medidas_corporales"]
)

router.include_router(
    empleados_dto_web.router,
    prefix="/web/empleados_dto",
    tags=["web_empleados_dto"]
)

# =====================================================
#                   MOBILE ROUTES
# =====================================================

router.include_router(
    clientes_movil.router,
    prefix="/movil/clientes",
    tags=["movil_clientes"]
)
