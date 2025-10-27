from fastapi import Form
from app.application.schemas.empresa_schema import EmpresaUpdate

def empresa_update_as_form(
    nombre: str | None = Form(None),
    ruc: str | None = Form(None),
    direccion: str | None = Form(None),
    telefono: str | None = Form(None),
    correo: str | None = Form(None),
) -> EmpresaUpdate:
    return EmpresaUpdate(
        nombre=nombre,
        ruc=ruc,
        direccion=direccion,
        telefono=telefono,
        correo=correo,
    )
