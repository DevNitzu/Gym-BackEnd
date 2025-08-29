from sqlalchemy.orm import Session
from app.domain.repositories.cliente_repository import ClienteRepository
from app.domain.models.cliente import Cliente
from typing import Optional, List

class ClienteRepositoryImpl(ClienteRepository):
    def __init__(self, db: Session):
        self.db = db

    async def create(self, cliente_data: dict) -> Cliente:
        db_cliente = Cliente(**cliente_data)
        self.db.add(db_cliente)
        self.db.commit()
        self.db.refresh(db_cliente)
        return db_cliente

    async def get_by_id(self, id_cliente: int) -> Optional[Cliente]:
        return self.db.query(Cliente).filter(Cliente.id_cliente == id_cliente).first()

    async def get_by_email(self, email: str) -> Optional[Cliente]:
        return self.db.query(Cliente).filter(Cliente.email == email).first()

    async def get_by_cedula(self, cedula: str) -> Optional[Cliente]:
        return self.db.query(Cliente).filter(Cliente.cedula == cedula).first()

    async def update(self, id_cliente: int, cliente_data: dict) -> Optional[Cliente]:
        db_cliente = self.db.query(Cliente).filter(Cliente.id_cliente == id_cliente).first()
        if db_cliente:
            for key, value in cliente_data.items():
                setattr(db_cliente, key, value)
            self.db.commit()
            self.db.refresh(db_cliente)
        return db_cliente

    async def delete(self, id_cliente: int) -> bool:
        db_cliente = self.db.query(Cliente).filter(Cliente.id_cliente == id_cliente).first()
        if db_cliente:
            self.db.delete(db_cliente)
            self.db.commit()
            return True
        return False

    async def get_all(self) -> List[Cliente]:
        return self.db.query(Cliente).all()