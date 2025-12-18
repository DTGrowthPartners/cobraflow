from fastapi import Request, HTTPException
from typing import Optional
from starlette.responses import RedirectResponse
from fastapi import Request, HTTPException
from typing import Optional

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
    user = request.session.get("user")
    if not user:
        raise HTTPException(status_code=303, headers={"Location": "/login"})
    return user