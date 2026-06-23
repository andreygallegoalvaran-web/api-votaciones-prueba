from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. URL de conexión a SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./votaciones.db"

# 2. El motor de la base de datos
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 3. La sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. La base para los modelos
Base = declarative_base()

# 5. AQUÍ ESTÁ LA SOLUCIÓN: La función get_db que main.py está buscando
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()