"""
Middleware de auditoría para FastAPI (CA4).
Intercepta automáticamente las solicitudes de escritura (POST, PUT, DELETE) en rutas críticas
y registra el ID del usuario, la fecha/hora, la ruta consumida y un resumen de la acción.
"""
import re
from datetime import datetime
# pyrefly: ignore [missing-import]
from starlette.middleware.base import BaseHTTPMiddleware
# pyrefly: ignore [missing-import]
from starlette.requests import Request
# pyrefly: ignore [missing-import]
from starlette.responses import Response
from Repositories.database import SessionLocal
from Models.audit_log import AuditLogDTO
from Utils.security import decode_access_token

# Rutas y métodos que se deben auditar
AUDITED_PREFIXES = ["/constructoras", "/properties", "/leads", "/sales"]
AUDITED_METHODS = {"POST", "PUT", "DELETE"}

# Mapeo de método HTTP a tipo de acción para el log
METHOD_TO_ACTION = {
    "POST": "CREATE",
    "PUT": "UPDATE",
    "DELETE": "DELETE",
}

# Regex para extraer el tipo de entidad y posible ID de la ruta
# Ejemplo: /constructoras/5 → entity_type="constructora", entity_id=5
ROUTE_ENTITY_PATTERN = re.compile(r"^/(constructoras|properties|leads|sales)(?:/(\d+))?")

# Mapeo de prefijo de ruta a nombre de entidad
ROUTE_TO_ENTITY = {
    "constructoras": "constructora",
    "properties": "property",
    "leads": "lead",
    "sales": "sale",
}


def _extract_user_id_from_request(request: Request) -> int | None:
    """Extrae el user_id del token JWT en el header Authorization, si existe."""
    auth_header = request.headers.get("authorization", "")
    if not auth_header.startswith("Bearer "):
        return None
    token = auth_header[7:]
    payload = decode_access_token(token)
    if payload and "sub" in payload:
        try:
            return int(payload["sub"])
        except (ValueError, TypeError):
            return None
    return None


def _build_summary(method: str, path: str, entity_type: str, entity_id: int | None) -> str:
    """Genera un resumen legible de la acción realizada."""
    action = METHOD_TO_ACTION.get(method, method)
    if entity_id:
        return f"{action} en {entity_type} (ID: {entity_id}) vía {method} {path}"
    return f"{action} en {entity_type} vía {method} {path}"


class AuditLogMiddleware(BaseHTTPMiddleware):
    """
    Middleware que intercepta solicitudes de escritura en rutas críticas
    y registra un log de auditoría en la base de datos.
    """

    async def dispatch(self, request: Request, call_next) -> Response:
        method = request.method
        path = request.url.path

        # Solo auditar métodos de escritura en rutas configuradas
        should_audit = (
            method in AUDITED_METHODS
            and any(path.startswith(prefix) for prefix in AUDITED_PREFIXES)
        )

        # Procesar la solicitud normalmente
        response: Response = await call_next(request)

        # Si corresponde auditar y la respuesta fue exitosa (2xx), registrar el log
        if should_audit and 200 <= response.status_code < 300:
            try:
                user_id = _extract_user_id_from_request(request)

                # Extraer tipo de entidad e ID del path
                match = ROUTE_ENTITY_PATTERN.match(path)
                entity_type = "unknown"
                entity_id = None
                if match:
                    route_key = match.group(1)
                    entity_type = ROUTE_TO_ENTITY.get(route_key, route_key)
                    if match.group(2):
                        entity_id = int(match.group(2))

                action = METHOD_TO_ACTION.get(method, method)
                # Para ventas, usar acción especial "SALE" en POST
                if entity_type == "sale" and method == "POST":
                    action = "SALE"

                summary = _build_summary(method, path, entity_type, entity_id)

                # Crear una sesión independiente para el log (no interferir con la transacción principal)
                db = SessionLocal()
                try:
                    log_entry = AuditLogDTO(
                        user_id=user_id,
                        action=action,
                        entity_type=entity_type,
                        entity_id=entity_id,
                        endpoint=path,
                        method=method,
                        summary=summary,
                        created_at=datetime.utcnow(),
                    )
                    db.add(log_entry)
                    db.commit()
                finally:
                    db.close()
            except Exception as e:
                # El log de auditoría no debe interrumpir el flujo normal de la aplicación
                print(f"AUDIT LOG ERROR: No se pudo registrar el log de auditoría: {e}")

        return response
