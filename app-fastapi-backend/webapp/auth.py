from fastapi import Request, HTTPException
from typing import Optional
from starlette.responses import RedirectResponse

# --- CREDENCIALES DE DEMO (Hardcoded) ---
DEMO_USER = "demo@dtgrowthpartners.com"
DEMO_PASSWORD = "demo123"

def authenticate_user(request: Request, email: str, password: str) -> bool:
    """
    Verifica las credenciales del usuario y, si son correctas,
    establece la sesión.
    """
    if email == DEMO_USER and password == DEMO_PASSWORD:
        request.session["user"] = email
        return True
    return False

def logout_user(request: Request):
    """
    Limpia la sesión del usuario.
    """
    request.session.clear()

def get_current_user(request: Request) -> Optional[str]:
    """
    Obtiene el usuario actual de la sesión.
    Si no hay usuario, devuelve None.
    """
    return request.session.get("user")

def login_required(request: Request):
    """
    Dependencia de FastAPI para proteger rutas.
    Si el usuario no está autenticado, redirige al login.
    """
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    return user