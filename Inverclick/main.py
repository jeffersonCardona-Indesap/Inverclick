from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Repositories.database import verify_db_connection_and_schema
from Models.Users import Users
from Models.Prefix import Prefix
from Models.Country import Country
from Controllers.UsersController import router as users_router
from Controllers.PrefixController import router as prefix_router
from Controllers.CountryController import router as country_router

# Verificar la conexión y estructura de la base de datos al arrancar
verify_db_connection_and_schema([Prefix, Country, Users])

app = FastAPI(
    title="Inverclick API",
    description="API para el semillero de investigación Inverclick",
    version="1.0.0",
)

# Configurar CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Modificar en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar el router de cada controlador
app.include_router(users_router)
app.include_router(prefix_router)
app.include_router(country_router)