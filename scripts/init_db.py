import sys
sys.path.append('..')

from app.infrastructure.database.base import Base, engine
from app.core.config import settings

def init_db():
    print("Creando tablas")
    Base.metadata.create_all(bind=engine)
    print("Las tablas han sido creadas exitosamente!")

if __name__ == "__main__":
    init_db()