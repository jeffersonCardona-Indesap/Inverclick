# pyrefly: ignore [missing-import]
from fastapi import FastAPI
# pyrefly: ignore [missing-import]
from fastapi.middleware.cors import CORSMiddleware
from Repositories.database import verify_db_connection_and_schema
from Controllers.UsersController import router as users_router
from Controllers.Prefixcontroller import router as prefix_router
from Controllers.AuthController import router as auth_router
from Controllers.ConstructorasController import router as constructoras_router
from Controllers.PropertiesController import router as properties_router
from Controllers.LeadsController import router as leads_router
from Controllers.SalesController import router as sales_router
from Utils.audit_log_middleware import AuditLogMiddleware

# Verificar la conexión y estructura de la base de datos al arrancar
verify_db_connection_and_schema()

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

# Registrar Middleware de Auditoría (CA4)
app.add_middleware(AuditLogMiddleware)

# Registrar el router de usuarios del controlador
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(prefix_router)
app.include_router(constructoras_router)
app.include_router(properties_router)
app.include_router(leads_router)
app.include_router(sales_router)
