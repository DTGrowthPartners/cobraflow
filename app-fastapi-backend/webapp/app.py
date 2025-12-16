from fastapi import FastAPI, Request, Depends, Form, HTTPException
from typing import Optional, List
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from datetime import datetime
import os
import json
from . import auth, services
from fastapi import HTTPException
from pydantic import BaseModel, Field
from ..generador import generar_cuenta_de_cobro

app = FastAPI(
    title="Demo Web App - Cuentas de Cobro",
    description="Interfaz web para la generación de cuentas de cobro.",
    version="1.0.0"
)

class Servicio(BaseModel):
    descripcion: str = Field(..., example="Desarrollo de landing page")
    cantidad: int = Field(..., example=1)
    precio_unitario: float = Field(..., example=500000)

class SolicitudCuenta(BaseModel):
    nickname_cliente: str = Field(..., example="experiencia_cartagena")
    valor: float = Field(..., example=2000000)
    servicios: List[Servicio]
    concepto: str = Field(..., example="Facturación de servicios de marketing")
    fecha: str = Field(default_factory=lambda: datetime.now().strftime("%d/%m/%Y"))
    servicio_proyecto: str = Field("", example="Desarrollo Web, Marketing Digital")

def get_client_data_local(nickname: str):
    try:
        with open(os.path.join(project_root, "clientes.json"), "r", encoding="utf-8") as f:
            clientes = json.load(f)
        return clientes.get(nickname)
    except FileNotFoundError:
        return None

# --- MIDDLEWARE Y CONFIGURACIÓN ---
SECRET_KEY = "tu-super-secreto-key-debe-cambiarse"
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

# --- MONTAJE DE ARCHIVOS ESTÁTICOS Y PLANTILLAS ---
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, '..'))

app.mount("/static", StaticFiles(directory=os.path.join(script_dir, "static")), name="static")
# Montar la carpeta 'creadas' para poder servir los PDFs generados
creadas_dir = os.path.join(project_root, "creadas")
os.makedirs(creadas_dir, exist_ok=True)
app.mount("/creadas", StaticFiles(directory=creadas_dir), name="creadas")
# Rutas para servir las bases
from fastapi.responses import FileResponse

@app.get("/bases/base.jpg")
async def get_base1():
    base_path = os.path.join(project_root, "base.jpg")
    if os.path.exists(base_path):
        return FileResponse(base_path)
    raise HTTPException(status_code=404, detail="File not found")

@app.get("/bases/Base2.jpg")
async def get_base2():
    base_path = os.path.join(project_root, "Base2.jpg")
    if os.path.exists(base_path):
        return FileResponse(base_path)
    raise HTTPException(status_code=404, detail="File not found")

@app.get("/bases/Base3.jpg")
async def get_base3():
    base_path = os.path.join(project_root, "Base3.jpg")
    if os.path.exists(base_path):
        return FileResponse(base_path)
    raise HTTPException(status_code=404, detail="File not found")

@app.get("/bases/Base4.jpg")
async def get_base4():
    base_path = os.path.join(project_root, "Base4.jpg")
    if os.path.exists(base_path):
        return FileResponse(base_path)
    raise HTTPException(status_code=404, detail="File not found")

@app.get("/bases/Base5.jpg")
async def get_base5():
    base_path = os.path.join(project_root, "Base5.jpg")
    if os.path.exists(base_path):
        return FileResponse(base_path)
    raise HTTPException(status_code=404, detail="File not found")

@app.get("/bases/Base6.jpg")
async def get_base6():
    base_path = os.path.join(project_root, "Base6.jpg")
    if os.path.exists(base_path):
        return FileResponse(base_path)
    raise HTTPException(status_code=404, detail="File not found")

templates = Jinja2Templates(directory=os.path.join(script_dir, "templates"))

# --- API ENDPOINTS ---
@app.post("/api/crear-cuenta/", summary="Crear una nueva cuenta de cobro")
async def crear_cuenta(solicitud: SolicitudCuenta):
    """
    Genera una cuenta de cobro para un cliente específico.
    """
    try:
        cliente_data = get_client_data_local(solicitud.nickname_cliente)

        if not cliente_data:
            raise HTTPException(
                status_code=404,
                detail=f"Cliente con nickname '{solicitud.nickname_cliente}' no encontrado."
            )

        servicios_dict = [s.dict() for s in solicitud.servicios]

        ruta_archivo_generado = generar_cuenta_de_cobro(
            nombre_cliente=cliente_data['nombre_completo'],
            identificacion=cliente_data['nit'],
            servicios=servicios_dict,
            concepto=solicitud.concepto,
            fecha=solicitud.fecha,
            servicio_proyecto=solicitud.servicio_proyecto if solicitud.servicio_proyecto else None
        )

        if not os.path.exists(ruta_archivo_generado):
            raise HTTPException(status_code=500, detail="Error: el archivo PDF no pudo ser creado.")

        return FileResponse(
            path=ruta_archivo_generado,
            media_type='application/pdf',
            filename=os.path.basename(ruta_archivo_generado)
        )
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ocurrió un error inesperado: {e}")

# --- RUTAS ---

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    if not auth.get_current_user(request):
        return RedirectResponse(url="/login", status_code=302)
    return RedirectResponse(url="/dashboard", status_code=302)

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    if auth.get_current_user(request):
        return RedirectResponse(url="/dashboard", status_code=302)
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login", response_class=HTMLResponse)
async def handle_login(request: Request, email: str = Form(...), password: str = Form(...)):
    if auth.authenticate_user(request, email, password):
        return RedirectResponse(url="/dashboard", status_code=302)
    return templates.TemplateResponse("login.html", {"request": request, "error": "Credenciales incorrectas"})

@app.get("/logout")
async def logout(request: Request):
    auth.logout_user(request)
    return RedirectResponse(url="/login", status_code=302)

# --- RUTAS API ---
@app.post("/api/add_service")
async def add_service(
    request: Request,
    nombre: str = Form(...),
    descripcion: str = Form(...),
    categoria: str = Form(...),
    user: str = Depends(auth.login_required)
):
    success = services.add_new_service(nombre, descripcion, categoria)
    if success:
        return {"success": True, "message": "Servicio añadido exitosamente"}
    else:
        return {"success": False, "message": "Error al añadir el servicio"}

@app.post("/api/add_client")
async def add_client(
    request: Request,
    nickname: str = Form(...),
    nombre_completo: str = Form(...),
    direccion: str = Form(...),
    nit: str = Form(...),
    user: str = Depends(auth.login_required)
):
    success = services.add_new_client(nickname, nombre_completo, direccion, nit)
    if success:
        return {"success": True, "message": "Cliente añadido exitosamente"}
    else:
        return {"success": False, "message": "Error al añadir el cliente"}

@app.get("/api/get_services")
async def get_services(request: Request, user: str = Depends(auth.login_required)):
    services_list = services.list_services()
    return {"services": services_list}

@app.get("/api/get_clients")
async def get_clients(request: Request, user: str = Depends(auth.login_required)):
    clients_list = services.list_clients()
    return {"clients": clients_list}

@app.post("/api/delete_invoice")
async def delete_invoice(
    request: Request,
    filename: str = Form(...),
    user: str = Depends(auth.login_required)
):
    """Endpoint para eliminar una factura generada"""
    success = services.delete_invoice_file(filename)
    if success:
        return {"success": True, "message": "Factura eliminada correctamente"}
    else:
        return {"success": False, "message": "Error al eliminar la factura"}

@app.post("/api/delete_multiple_invoices")
async def delete_multiple_invoices(
    request: Request,
    filenames: str = Form(...),  # Lista separada por comas
    user: str = Depends(auth.login_required)
):
    """Endpoint para eliminar múltiples facturas generadas"""
    filename_list = [f.strip() for f in filenames.split(',') if f.strip()]
    results = services.delete_multiple_invoices(filename_list)
    successful = sum(1 for r in results.values() if r)
    total = len(results)
    if successful == total:
        return {"success": True, "message": f"{successful} facturas eliminadas correctamente"}
    elif successful > 0:
        return {"success": True, "message": f"{successful} de {total} facturas eliminadas correctamente"}
    else:
        return {"success": False, "message": "Error al eliminar las facturas"}

@app.post("/api/edit_client")
async def edit_client(
    request: Request,
    nickname: str = Form(...),
    nombre_completo: str = Form(...),
    direccion: str = Form(...),
    nit: str = Form(...),
    user: str = Depends(auth.login_required)
):
    success = services.edit_client(nickname, nombre_completo, direccion, nit)
    if success:
        return {"success": True, "message": "Cliente editado exitosamente"}
    else:
        return {"success": False, "message": "Error al editar el cliente"}

@app.post("/api/delete_client")
async def delete_client(
    request: Request,
    nickname: str = Form(...),
    user: str = Depends(auth.login_required)
):
    success = services.delete_client(nickname)
    if success:
        return {"success": True, "message": "Cliente eliminado exitosamente"}
    else:
        return {"success": False, "message": "Error al eliminar el cliente"}

@app.post("/api/edit_service")
async def edit_service(
    request: Request,
    index: int = Form(...),
    nombre: str = Form(...),
    descripcion: str = Form(...),
    categoria: str = Form(...),
    user: str = Depends(auth.login_required)
):
    success = services.edit_service(index, nombre, descripcion, categoria)
    if success:
        return {"success": True, "message": "Servicio editado exitosamente"}
    else:
        return {"success": False, "message": "Error al editar el servicio"}

@app.post("/api/delete_service")
async def delete_service(
    request: Request,
    index: int = Form(...),
    user: str = Depends(auth.login_required)
):
    success = services.delete_service(index)
    if success:
        return {"success": True, "message": "Servicio eliminado exitosamente"}
    else:
        return {"success": False, "message": "Error al eliminar el servicio"}

@app.post("/api/set_base")
async def set_base(
    request: Request,
    base_name: str = Form(...),
    user: str = Depends(auth.login_required)
):
    # Validar que el archivo existe
    valid_bases = ["base.jpg", "Base2.jpg", "Base3.jpg", "Base4.jpg", "Base5.jpg", "Base6.jpg"]
    if base_name not in valid_bases:
        return {"success": False, "message": "Base no válida"}

    base_path = os.path.join(project_root, base_name)
    if not os.path.exists(base_path):
        return {"success": False, "message": "Archivo base no encontrado"}

    # Guardar la base actual en un archivo
    config_path = os.path.join(project_root, "base_actual.txt")
    colors_path = os.path.join(project_root, "base_colors.txt")
    try:
        with open(config_path, "w") as f:
            f.write(base_name)
        # Resetear colores al cambiar base
        if os.path.exists(colors_path):
            os.remove(colors_path)
        return {"success": True, "message": f"Base cambiada a {base_name}"}
    except Exception as e:
        return {"success": False, "message": f"Error al guardar configuración: {str(e)}"}

@app.get("/api/get_base")
async def get_base(request: Request, user: str = Depends(auth.login_required)):
    config_path = os.path.join(project_root, "base_actual.txt")
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            base_name = f.read().strip()
        return {"base": base_name}
    else:
        return {"base": "base.jpg"}  # Default

@app.post("/api/set_colors")
async def set_colors(
    primary_color: str = Form(...),
    secondary_color: Optional[str] = Form(None)
):
    # Guardar los colores en un archivo
    colors_path = os.path.join(project_root, "base_colors.txt")
    try:
        content = f"{primary_color}"
        if secondary_color:
            content += f"\n{secondary_color}"
        with open(colors_path, "w") as f:
            f.write(content)
        return {"success": True, "message": "Colores guardados"}
    except Exception as e:
        return {"success": False, "message": f"Error al guardar colores: {str(e)}"}

@app.get("/api/get_colors")
async def get_colors(request: Request, user: str = Depends(auth.login_required)):
    colors_path = os.path.join(project_root, "base_colors.txt")
    if os.path.exists(colors_path):
        with open(colors_path, "r") as f:
            lines = f.readlines()
            if len(lines) >= 2:
                primary = lines[0].strip()
                secondary = lines[1].strip()
                return {"primary": primary, "secondary": secondary}
    return {"primary": "#005F99", "secondary": "#FFFFFF"}  # Default

@app.get("/api/get_fonts")
async def get_fonts(request: Request, user: str = Depends(auth.login_required)):
    fonts_list = services.list_fonts()
    return {"fonts": fonts_list}

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, user: str = Depends(auth.login_required)):
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
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "user": user,
        "clients": clients,
        "services": services_list,
        "fonts": fonts,
        "history": history,
        "success_message": success_message,
        "generated_pdf_url": generated_pdf_url
    })

@app.post("/dashboard/generate", response_class=HTMLResponse)
async def generate_invoice_request(request: Request, user: str = Depends(auth.login_required)):
    form_data = await request.form()
    
    try:
        # Extraer datos del formulario
        nickname_cliente = form_data.get("nickname_cliente")
        servicio_proyecto = form_data.get("servicio_proyecto")
        nombre_empresa = form_data.get("nombre_empresa", "")
        fuente_seleccionada = form_data.get("fuente_seleccionada", "HelveticaNeue.ttf")

        # Recolectar los servicios dinámicamente
        servicios = []
        i = 1
        while True:
            desc = form_data.get(f"servicio_descripcion_{i}")
            cant = form_data.get(f"servicio_cantidad_{i}")
            precio = form_data.get(f"servicio_precio_{i}")

            if not desc or not cant or not precio:
                break # Termina el bucle si falta algún campo del servicio

            servicios.append({
                "descripcion": desc,
                "cantidad": int(cant),
                "precio_unitario": float(precio)
            })
            i += 1

        if not nickname_cliente or not servicios:
            raise ValueError("El cliente y al menos un servicio son requeridos.")

        # Llamar al servicio para generar el PDF
        pdf_path = services.generate_invoice_service(
            nickname_cliente=nickname_cliente,
            servicios=servicios,
            concepto="",  # Eliminado el concepto general como se solicitó
            fecha=datetime.now().strftime("%d/%m/%Y"),
            servicio_proyecto=servicio_proyecto,
            nombre_empresa=nombre_empresa,
            fuente_seleccionada=fuente_seleccionada
        )
        
        pdf_filename = os.path.basename(pdf_path)
        generated_pdf_url = f"/creadas/{pdf_filename}"
        success_message = f"¡Cuenta de cobro generada exitosamente! Archivo: {pdf_filename}"

    except Exception as e:
        # En caso de error, renderizar el dashboard con un mensaje de error
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

    # Redirigir para evitar resubmission
    return RedirectResponse(url=f"/dashboard?success=1&pdf={pdf_filename}", status_code=302)

# --- NUEVAS RUTAS PARA MANEJO DE SERVICIOS Y CLIENTES ---
@app.post("/api/add_service")
async def add_service(
    request: Request,
    nombre: str = Form(...),
    descripcion: str = Form(...),
    categoria: str = Form(...),
    user: str = Depends(auth.login_required)
):
    success = services.add_new_service(nombre, descripcion, categoria)
    if success:
        return {"success": True, "message": "Servicio añadido exitosamente"}
    else:
        return {"success": False, "message": "Error al añadir el servicio"}

@app.post("/api/add_client")
async def add_client(
    request: Request,
    nickname: str = Form(...),
    nombre_completo: str = Form(...),
    direccion: str = Form(...),
    nit: str = Form(...),
    user: str = Depends(auth.login_required)
):
    success = services.add_new_client(nickname, nombre_completo, direccion, nit)
    if success:
        return {"success": True, "message": "Cliente añadido exitosamente"}
    else:
        return {"success": False, "message": "Error al añadir el cliente"}

@app.get("/api/get_services")
async def get_services(request: Request, user: str = Depends(auth.login_required)):
    services_list = services.list_services()
    return {"services": services_list}

@app.get("/api/get_clients")
async def get_clients(request: Request, user: str = Depends(auth.login_required)):
    clients_list = services.list_clients()
    return {"clients": clients_list}

@app.post("/api/delete_invoice")
async def delete_invoice(
    request: Request,
    filename: str = Form(...),
    user: str = Depends(auth.login_required)
):
    """Endpoint para eliminar una factura generada"""
    success = services.delete_invoice_file(filename)
    if success:
        return {"success": True, "message": "Factura eliminada correctamente"}
    else:
        return {"success": False, "message": "Error al eliminar la factura"}

@app.post("/api/edit_client")
async def edit_client(
    request: Request,
    nickname: str = Form(...),
    nombre_completo: str = Form(...),
    direccion: str = Form(...),
    nit: str = Form(...),
    user: str = Depends(auth.login_required)
):
    success = services.edit_client(nickname, nombre_completo, direccion, nit)
    if success:
        return {"success": True, "message": "Cliente editado exitosamente"}
    else:
        return {"success": False, "message": "Error al editar el cliente"}

@app.post("/api/delete_client")
async def delete_client(
    request: Request,
    nickname: str = Form(...),
    user: str = Depends(auth.login_required)
):
    success = services.delete_client(nickname)
    if success:
        return {"success": True, "message": "Cliente eliminado exitosamente"}
    else:
        return {"success": False, "message": "Error al eliminar el cliente"}

@app.post("/api/edit_service")
async def edit_service(
    request: Request,
    index: int = Form(...),
    nombre: str = Form(...),
    descripcion: str = Form(...),
    categoria: str = Form(...),
    user: str = Depends(auth.login_required)
):
    success = services.edit_service(index, nombre, descripcion, categoria)
    if success:
        return {"success": True, "message": "Servicio editado exitosamente"}
    else:
        return {"success": False, "message": "Error al editar el servicio"}

@app.post("/api/delete_service")
async def delete_service(
    request: Request,
    index: int = Form(...),
    user: str = Depends(auth.login_required)
):
    success = services.delete_service(index)
    if success:
        return {"success": True, "message": "Servicio eliminado exitosamente"}
    else:
        return {"success": False, "message": "Error al eliminar el servicio"}

@app.post("/api/set_base")
async def set_base(
    request: Request,
    base_name: str = Form(...),
    user: str = Depends(auth.login_required)
):
    # Validar que el archivo existe
    valid_bases = ["base.jpg", "Base2.jpg", "Base3.jpg", "Base4.jpg", "Base5.jpg", "Base6.jpg"]
    if base_name not in valid_bases:
        return {"success": False, "message": "Base no válida"}

    base_path = os.path.join(project_root, base_name)
    if not os.path.exists(base_path):
        return {"success": False, "message": "Archivo base no encontrado"}

    # Guardar la base actual en un archivo
    config_path = os.path.join(project_root, "base_actual.txt")
    colors_path = os.path.join(project_root, "base_colors.txt")
    try:
        with open(config_path, "w") as f:
            f.write(base_name)
        # Resetear colores al cambiar base
        if os.path.exists(colors_path):
            os.remove(colors_path)
        return {"success": True, "message": f"Base cambiada a {base_name}"}
    except Exception as e:
        return {"success": False, "message": f"Error al guardar configuración: {str(e)}"}

@app.get("/api/get_base")
async def get_base(request: Request, user: str = Depends(auth.login_required)):
    config_path = os.path.join(project_root, "base_actual.txt")
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            base_name = f.read().strip()
        return {"base": base_name}
    else:
        return {"base": "base.jpg"}  # Default

@app.post("/api/set_colors")
async def set_colors(
    primary_color: str = Form(...),
    secondary_color: Optional[str] = Form(None)
):
    # Guardar los colores en un archivo
    colors_path = os.path.join(project_root, "base_colors.txt")
    try:
        content = f"{primary_color}"
        if secondary_color:
            content += f"\n{secondary_color}"
        with open(colors_path, "w") as f:
            f.write(content)
        return {"success": True, "message": "Colores guardados"}
    except Exception as e:
        return {"success": False, "message": f"Error al guardar colores: {str(e)}"}

@app.get("/api/get_colors")
async def get_colors(request: Request, user: str = Depends(auth.login_required)):
    colors_path = os.path.join(project_root, "base_colors.txt")
    if os.path.exists(colors_path):
        with open(colors_path, "r") as f:
            lines = f.readlines()
            if len(lines) >= 2:
                primary = lines[0].strip()
                secondary = lines[1].strip()
                return {"primary": primary, "secondary": secondary}
    return {"primary": "#005F99", "secondary": "#FFFFFF"}  # Default

@app.get("/api/get_fonts")
async def get_fonts(request: Request, user: str = Depends(auth.login_required)):
    fonts_list = services.list_fonts()
    return {"fonts": fonts_list}

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, user: str = Depends(auth.login_required)):
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
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "user": user,
        "clients": clients,
        "services": services_list,
        "fonts": fonts,
        "history": history,
        "success_message": success_message,
        "generated_pdf_url": generated_pdf_url
    })

@app.post("/dashboard/generate", response_class=HTMLResponse)
async def generate_invoice_request(request: Request, user: str = Depends(auth.login_required)):
    form_data = await request.form()
    
    try:
        # Extraer datos del formulario
        nickname_cliente = form_data.get("nickname_cliente")
        servicio_proyecto = form_data.get("servicio_proyecto")
        nombre_empresa = form_data.get("nombre_empresa", "")
        fuente_seleccionada = form_data.get("fuente_seleccionada", "HelveticaNeue.ttf")

        # Recolectar los servicios dinámicamente
        servicios = []
        i = 1
        while True:
            desc = form_data.get(f"servicio_descripcion_{i}")
            cant = form_data.get(f"servicio_cantidad_{i}")
            precio = form_data.get(f"servicio_precio_{i}")

            if not desc or not cant or not precio:
                break # Termina el bucle si falta algún campo del servicio

            servicios.append({
                "descripcion": desc,
                "cantidad": int(cant),
                "precio_unitario": float(precio)
            })
            i += 1

        if not nickname_cliente or not servicios:
            raise ValueError("El cliente y al menos un servicio son requeridos.")

        # Llamar al servicio para generar el PDF
        pdf_path = services.generate_invoice_service(
            nickname_cliente=nickname_cliente,
            servicios=servicios,
            concepto="",  # Eliminado el concepto general como se solicitó
            fecha=datetime.now().strftime("%d/%m/%Y"),
            servicio_proyecto=servicio_proyecto,
            nombre_empresa=nombre_empresa,
            fuente_seleccionada=fuente_seleccionada
        )
        
        pdf_filename = os.path.basename(pdf_path)
        generated_pdf_url = f"/creadas/{pdf_filename}"
        success_message = f"¡Cuenta de cobro generada exitosamente! Archivo: {pdf_filename}"

    except Exception as e:
        # En caso de error, renderizar el dashboard con un mensaje de error
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

    # Redirigir para evitar resubmission
    return RedirectResponse(url=f"/dashboard?success=1&pdf={pdf_filename}", status_code=302)

# --- NUEVAS RUTAS PARA MANEJO DE SERVICIOS Y CLIENTES ---
@app.post("/api/add_service")
async def add_service(
    request: Request,
    nombre: str = Form(...),
    descripcion: str = Form(...),
    categoria: str = Form(...),
    user: str = Depends(auth.login_required)
):
    success = services.add_new_service(nombre, descripcion, categoria)
    if success:
        return {"success": True, "message": "Servicio añadido exitosamente"}
    else:
        return {"success": False, "message": "Error al añadir el servicio"}

@app.post("/api/add_client")
async def add_client(
    request: Request,
    nickname: str = Form(...),
    nombre_completo: str = Form(...),
    direccion: str = Form(...),
    nit: str = Form(...),
    user: str = Depends(auth.login_required)
):
    success = services.add_new_client(nickname, nombre_completo, direccion, nit)
    if success:
        return {"success": True, "message": "Cliente añadido exitosamente"}
    else:
        return {"success": False, "message": "Error al añadir el cliente"}

@app.get("/api/get_services")
async def get_services(request: Request, user: str = Depends(auth.login_required)):
    services_list = services.list_services()
    return {"services": services_list}

@app.get("/api/get_clients")
async def get_clients(request: Request, user: str = Depends(auth.login_required)):
    clients_list = services.list_clients()
    return {"clients": clients_list}

@app.post("/api/delete_invoice")
async def delete_invoice(
    request: Request,
    filename: str = Form(...),
    user: str = Depends(auth.login_required)
):
    """Endpoint para eliminar una factura generada"""
    success = services.delete_invoice_file(filename)
    if success:
        return {"success": True, "message": "Factura eliminada correctamente"}
    else:
        return {"success": False, "message": "Error al eliminar la factura"}

@app.post("/api/edit_client")
async def edit_client(
    request: Request,
    nickname: str = Form(...),
    nombre_completo: str = Form(...),
    direccion: str = Form(...),
    nit: str = Form(...),
    user: str = Depends(auth.login_required)
):
    success = services.edit_client(nickname, nombre_completo, direccion, nit)
    if success:
        return {"success": True, "message": "Cliente editado exitosamente"}
    else:
        return {"success": False, "message": "Error al editar el cliente"}

@app.post("/api/delete_client")
async def delete_client(
    request: Request,
    nickname: str = Form(...),
    user: str = Depends(auth.login_required)
):
    success = services.delete_client(nickname)
    if success:
        return {"success": True, "message": "Cliente eliminado exitosamente"}
    else:
        return {"success": False, "message": "Error al eliminar el cliente"}

@app.post("/api/edit_service")
async def edit_service(
    request: Request,
    index: int = Form(...),
    nombre: str = Form(...),
    descripcion: str = Form(...),
    categoria: str = Form(...),
    user: str = Depends(auth.login_required)
):
    success = services.edit_service(index, nombre, descripcion, categoria)
    if success:
        return {"success": True, "message": "Servicio editado exitosamente"}
    else:
        return {"success": False, "message": "Error al editar el servicio"}

@app.post("/api/delete_service")
async def delete_service(
    request: Request,
    index: int = Form(...),
    user: str = Depends(auth.login_required)
):
    success = services.delete_service(index)
    if success:
        return {"success": True, "message": "Servicio eliminado exitosamente"}
    else:
        return {"success": False, "message": "Error al eliminar el servicio"}

@app.post("/api/set_base")
async def set_base(
    request: Request,
    base_name: str = Form(...),
    user: str = Depends(auth.login_required)
):
    # Validar que el archivo existe
    valid_bases = ["base.jpg", "Base2.jpg", "Base3.jpg", "Base4.jpg"]
    if base_name not in valid_bases:
        return {"success": False, "message": "Base no válida"}

    base_path = os.path.join(project_root, base_name)
    if not os.path.exists(base_path):
        return {"success": False, "message": "Archivo base no encontrado"}

    # Guardar la base actual en un archivo
    config_path = os.path.join(project_root, "base_actual.txt")
    try:
        with open(config_path, "w") as f:
            f.write(base_name)
        return {"success": True, "message": f"Base cambiada a {base_name}"}
    except Exception as e:
        return {"success": False, "message": f"Error al guardar configuración: {str(e)}"}

@app.get("/api/get_base")
async def get_base(request: Request, user: str = Depends(auth.login_required)):
    config_path = os.path.join(project_root, "base_actual.txt")
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            base_name = f.read().strip()
        return {"base": base_name}
    else:
        return {"base": "base.jpg"}  # Default

if __name__ == "__main__":
    import uvicorn
    # Se asume que este comando se ejecuta desde el directorio raíz del proyecto
    # Ejemplo: python -m webapp.app
    uvicorn.run("webapp.app:app", host="0.0.0.0", port=8001, reload=True)