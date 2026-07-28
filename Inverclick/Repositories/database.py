# database.py
import os
from xml.parsers.expat import model
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from dotenv import load_dotenv

# Cargar las variables de entorno
load_dotenv()

# Obtener la URL (Asegúrate de que no devuelva None)
DATABASE_URL = os.getenv("DATABASE_URL")

# Crear el engine. echo=True imprimirá las consultas SQL en la consola (útil en desarrollo)
engine = create_engine(DATABASE_URL, echo=True)

# Configurar la fábrica de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Clase base para definir nuestros modelos (Sintaxis SQLAlchemy 2.0)
class Base(DeclarativeBase):
    pass

# Dependencia para inyectar la sesión en tus rutas o servicios
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Función para verificar la conexión y la estructura de las tablas sin alterarlas
def verify_db_connection_and_schema(models_to_check: list) -> bool:
    
    
    try:
        # 1. Verificar la conexión básica ejecutando una consulta rápida
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            print("DATABASE: Conexión establecida con éxito.")
            
            # 2. Inspeccionar la base de datos
            inspector = inspect(engine)
            all_ok = True
            
            # Verificar cada modelo en la lista
            for model in models_to_check:
                table_name = model.__tablename__
                
                # Verificar si la tabla existe
                if not inspector.has_table(table_name):
                    print(f"DATABASE ERROR: La tabla '{table_name}' no existe en la base de datos.")
                    all_ok = False
                    continue
                
                # 3. Verificar que las columnas coincidan
                db_columns = {col["name"] for col in inspector.get_columns(table_name)}
                model_columns = {col.name for col in model.__table__.columns}

                columnas_faltantes = model_columns - db_columns

                if columnas_faltantes:
                    print(f"DATABASE ERROR: En '{table_name}' faltan columnas en la BD: {columnas_faltantes}")
                    all_ok = False
                else:   
                    print(f"DATABASE: Tabla '{table_name}' verificada y correcta.")

            return all_ok
            
    except Exception as e:
        print(f"DATABASE ERROR: Fallo al verificar la conexión o estructura: {e}")
        return False

