"""
Web routes for CobraFlow application.
This module provides all web-related routes (/, /login, /dashboard, /logout)
and should be integrated into the main FastAPI app.
"""

from fastapi import APIRouter, Request, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
import os
import json
from datetime import datetime

from . import auth, services

# Create router for web routes
web_router = APIRouter()

# Configuration
SECRET_KEY = "tu-super-secreto-key-debe-cambiarse"

# Get script directory
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, '..'))

# Setup templates
templates = Jinja2Templates(directory=os.path.join(script_dir, "templates"))


@web_router.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Root route - shows landing page or redirects to dashboard if logged in."""
    if auth.get_current_user(request):
        return RedirectResponse(url="/dashboard", status_code=302)
    return templates.TemplateResponse("index.html", {"request": request})


@web_router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Login page."""
    if auth.get_current_user(request):
        return RedirectResponse(url="/dashboard", status_code=302)
    return templates.TemplateResponse("login.html", {"request": request})


@web_router.post("/login", response_class=HTMLResponse)
async def handle_login(request: Request, email: str = Form(...), password: str = Form(...)):
    """Handle login form submission."""
    if auth.authenticate_user(request, email, password):
        return RedirectResponse(url="/dashboard", status_code=302)
    return templates.TemplateResponse("login.html", {"request": request, "error": "Credenciales incorrectas"})


@web_router.get("/logout")
async def logout(request: Request):
    """Logout and redirect to login page."""
    auth.logout_user(request)
    return RedirectResponse(url="/login", status_code=302)


@web_router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, user: str = Depends(auth.login_required)):
    """Dashboard page - requires authentication."""
    clients = services.list_clients()
    history = services.list_generated_invoices()
    fonts = services.list_fonts()
    services_list = services.list_services()
    
    success_message = None
    generated_pdf_url = None
    if request.query_params.get("success") == "1":
        pdf_filename = request.query_params.get("pdf")
        if pdf_filename:
            success_message = f"¡Cuenta de cobro generada exitosamente! Archivo: {pdf_filename}"
            generated_pdf_url = f"/creadas/{pdf_filename}"
    
    api_base_url = str(request.base_url).rstrip("/")
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "user": user,
        "clients": clients,
        "services": services_list,
        "fonts": fonts,
        "history": history,
        "success_message": success_message,
        "generated_pdf_url": generated_pdf_url,
        "api_base_url": api_base_url
    })


@web_router.get("/template-editor", response_class=HTMLResponse)
async def template_editor(request: Request, user: str = Depends(auth.login_required)):
    """Visual template editor page - requires authentication."""
    return templates.TemplateResponse("template_editor.html", {
        "request": request,
        "user": user
    })

@web_router.get("/template_editor", include_in_schema=False)
async def template_editor_alias(request: Request, user: str = Depends(auth.login_required)):
    return RedirectResponse(url="/template-editor", status_code=302)

@web_router.get("/template_editor.html", include_in_schema=False)
async def template_editor_html_alias(request: Request, user: str = Depends(auth.login_required)):
    return RedirectResponse(url="/template-editor", status_code=302)


@web_router.post("/dashboard/generate", response_class=HTMLResponse)
async def generate_invoice_request(request: Request, user: str = Depends(auth.login_required)):
    """Generate invoice from dashboard form."""
    print("="*80)
    print("DEBUG WEB_ROUTES - INICIO DE GENERATE_INVOICE_REQUEST")
    print("="*80)
    form_data = await request.form()
    print(f"DEBUG WEB_ROUTES - Form data keys: {list(form_data.keys())}")

    try:
        # Extract form data
        nickname_cliente = form_data.get("nickname_cliente")
        servicio_proyecto = form_data.get("servicio_proyecto")
        nombre_empresa = ""
        fuente_seleccionada = form_data.get("fuente_seleccionada", "HelveticaNeue.ttf")

        # Extract new fields
        tipo_operacion = form_data.get("tipo_operacion", "natural-natural")
        moneda = form_data.get("moneda", "COP")
        plazo_pago = form_data.get("plazo_pago", "30")
        texto_legal = form_data.get("texto_legal", "")

        # DEBUG: Imprimir valores recibidos
        print(f"DEBUG - tipo_operacion: {tipo_operacion}")
        print(f"DEBUG - moneda: {moneda}")
        print(f"DEBUG - plazo_pago: {plazo_pago}")
        print(f"DEBUG - texto_legal: {texto_legal[:100] if texto_legal else 'VACIO'}")
        
        # Forzar valores por defecto si no se reciben correctamente
        if not plazo_pago:
            print("ADVERTENCIA: plazo_pago no se recibió correctamente, usando valor por defecto")
            plazo_pago = "30"
        
        # Parse retenciones
        retenciones_json = form_data.get("retenciones_aplicadas", "[]")
        print(f"DEBUG - retenciones_json: {retenciones_json}")
        retenciones = []
        try:
            retenciones = json.loads(retenciones_json) if retenciones_json else []
            print(f"DEBUG - retenciones parseadas: {retenciones}")
        except Exception as e:
            print(f"DEBUG - Error parseando retenciones: {e}")
            retenciones = []
        
        if not isinstance(retenciones, list):
            print("ADVERTENCIA: retenciones no es una lista válida, inicializando como vacía")
            retenciones = []
        
        # Load saved billing data
        billing_path = os.path.join(project_root, "billing_data.json")
        if os.path.exists(billing_path):
            with open(billing_path, "r", encoding="utf-8") as f:
                billing_data = json.load(f)
        else:
            billing_data = {
                "emisor_nombre": "Dairo Tralasviña",
                "emisor_cedula": "1143397563",
                "emisor_telefono": "+57 3007189383",
                "emisor_email": "Dairo@dtgrowthpartners.com",
                "emisor_ciudad": "Cartagena, Colombia",
                "cuenta_bancolombia": "78841707710",
                "nequi_daviplata": "+57 3007189383",
                "nota_pago": "Se solicita que el pago sea realizado a la mayor brevedad posible",
                "firma": "Dairo Tralasviña,",
            }
        
        emisor_nombre = billing_data["emisor_nombre"]
        emisor_cedula = billing_data["emisor_cedula"]
        emisor_telefono = billing_data["emisor_telefono"]
        emisor_email = billing_data["emisor_email"]
        emisor_ciudad = billing_data["emisor_ciudad"]
        cuenta_bancolombia = billing_data["cuenta_bancolombia"]
        nequi_daviplata = billing_data["nequi_daviplata"]
        nota_pago = billing_data["nota_pago"]
        firma = billing_data["firma"]
        
        # Collect services dynamically
        servicios = []
        i = 1
        while True:
            desc = form_data.get(f"servicio_descripcion_{i}")
            cant = form_data.get(f"servicio_cantidad_{i}")
            precio = form_data.get(f"servicio_precio_{i}")
            
            if not desc or not cant or not precio:
                break
            
            servicios.append({
                "descripcion": desc,
                "cantidad": int(cant),
                "precio_unitario": float(precio)
            })
            i += 1
        
        if not nickname_cliente or not servicios:
            raise ValueError("El cliente y al menos un servicio son requeridos.")
        
        # Generate PDF
        pdf_path = services.generate_invoice_service(
            nickname_cliente=nickname_cliente,
            servicios=servicios,
            concepto="",
            fecha=datetime.now().strftime("%d/%m/%Y"),
            servicio_proyecto=servicio_proyecto,
            nombre_empresa=nombre_empresa,
            fuente_seleccionada=fuente_seleccionada,
            emisor_nombre=emisor_nombre,
            emisor_cedula=emisor_cedula,
            emisor_telefono=emisor_telefono,
            emisor_email=emisor_email,
            emisor_ciudad=emisor_ciudad,
            cuenta_bancolombia=cuenta_bancolombia,
            nequi_daviplata=nequi_daviplata,
            nota_pago=nota_pago,
            firma=firma,
            tipo_operacion=tipo_operacion,
            moneda=moneda,
            plazo_pago=plazo_pago,
            texto_legal=texto_legal,
            retenciones=retenciones
        )
        
        pdf_filename = os.path.basename(pdf_path)
        
    except Exception as e:
        # On error, render dashboard with error message
        clients = services.list_clients()
        history = services.list_generated_invoices()
        services_list = services.list_services()
        return templates.TemplateResponse("dashboard.html", {
            "request": request,
            "user": user,
            "clients": clients,
            "services": services_list,
            "history": history,
            "error_message": f"Error al generar la cuenta: {e}"
        })
    
    # Redirect to avoid resubmission
    return RedirectResponse(url=f"/dashboard?success=1&pdf={pdf_filename}", status_code=302)


def register_web_routes(app):
    """
    Register web routes and middleware to the main FastAPI app.

    Args:
        app: FastAPI application instance
    """
    # Add session middleware if not already added
    from starlette.middleware.sessions import SessionMiddleware as SM
    has_session = any(isinstance(middleware, SM) for middleware in app.user_middleware)
    if not has_session:
        app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

    # Create creadas directory if it doesn't exist
    creadas_dir = os.path.join(project_root, "creadas")
    os.makedirs(creadas_dir, exist_ok=True)

    # Include web router
    app.include_router(web_router)
    
    # Add base image routes
    @app.get("/bases/base.jpg")
    async def get_base1():
        base_path = os.path.join(project_root, "base.jpg")
        if os.path.exists(base_path):
            from fastapi.responses import FileResponse
            return FileResponse(base_path)
        raise HTTPException(status_code=404, detail="File not found")
    
    @app.get("/bases/Base2.jpg")
    async def get_base2():
        base_path = os.path.join(project_root, "Base2.jpg")
        if os.path.exists(base_path):
            from fastapi.responses import FileResponse
            return FileResponse(base_path)
        raise HTTPException(status_code=404, detail="File not found")
    
    @app.get("/bases/Base3.jpg")
    async def get_base3():
        base_path = os.path.join(project_root, "Base3.jpg")
        if os.path.exists(base_path):
            from fastapi.responses import FileResponse
            return FileResponse(base_path)
        raise HTTPException(status_code=404, detail="File not found")
    
    @app.get("/bases/Base4.jpg")
    async def get_base4():
        base_path = os.path.join(project_root, "Base4.jpg")
        if os.path.exists(base_path):
            from fastapi.responses import FileResponse
            return FileResponse(base_path)
        raise HTTPException(status_code=404, detail="File not found")
    
    @app.get("/bases/Base5.jpg")
    async def get_base5():
        base_path = os.path.join(project_root, "Base5.jpg")
        if os.path.exists(base_path):
            from fastapi.responses import FileResponse
            return FileResponse(base_path)
        raise HTTPException(status_code=404, detail="File not found")
    
    @app.get("/bases/Base6.jpg")
    async def get_base6():
        base_path = os.path.join(project_root, "Base6.jpg")
        if os.path.exists(base_path):
            from fastapi.responses import FileResponse
            return FileResponse(base_path)
        raise HTTPException(status_code=404, detail="File not found")
