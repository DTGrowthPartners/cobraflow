import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Request, Depends, Form
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from generador import generar_cuenta_de_cobro
from datetime import datetime
import json
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path

app = FastAPI(
    title="API de Cuentas de Cobro",
    description="Una API para generar cuentas de cobro en formato PDF.",
    version="3.0.0"
)

# Configurar CORS para permitir requests desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Desarrollo local Vite
        "http://localhost:8080",  # Desarrollo local alternativo
        "http://localhost:3000",  # Alternativa desarrollo
        "https://cobraflow.co",   # Producción
        "https://www.cobraflow.co"  # Producción con www
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurar archivos estáticos y plantillas
BASE_DIR = Path(__file__).resolve().parent

# Servir archivos estáticos: /static/...
app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "webapp" / "static"),
    name="static"
)

# Servir archivos PDF generados: /creadas/...
creadas_dir = BASE_DIR / "creadas"
creadas_dir.mkdir(exist_ok=True)
app.mount(
    "/creadas",
    StaticFiles(directory=creadas_dir),
    name="creadas"
)

# Plantillas: webapp/templates/*.html
templates = Jinja2Templates(directory=str(BASE_DIR / "webapp" / "templates"))

# Importar y registrar rutas web (landing, login, dashboard)
from webapp import web_routes
web_routes.register_web_routes(app)

# Importar módulos para las rutas API
from webapp import auth, services

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
        with open("clientes.json", "r", encoding="utf-8") as f:
            clientes = json.load(f)
        return clientes.get(nickname)
    except FileNotFoundError:
        return None

@app.post("/crear-cuenta/", summary="Crear una nueva cuenta de cobro")
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

@app.post("/api/crear-cuenta-simple/", summary="Crear cuenta de cobro sin cliente previo")
async def crear_cuenta_simple(solicitud: SolicitudCuenta):
    """
    Genera una cuenta de cobro sin necesidad de tener un cliente pre-registrado.
    Usa el nickname_cliente como nombre del cliente directamente.
    """
    try:
        servicios_dict = [s.dict() for s in solicitud.servicios]
        
        # Usar el nickname como nombre del cliente
        nombre_cliente = solicitud.nickname_cliente
        # Generar un NIT/ID temporal basado en el timestamp
        identificacion = f"ID-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        ruta_archivo_generado = generar_cuenta_de_cobro(
            nombre_cliente=nombre_cliente,
            identificacion=identificacion,
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

# Ruta para servir index.html (ya manejada por web_routes)
# @app.get("/", response_class=HTMLResponse)
# async def read_root(request: Request):
#     return templates.TemplateResponse("index.html", {"request": request})

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

    base_path = os.path.join(BASE_DIR, base_name)
    if not os.path.exists(base_path):
        return {"success": False, "message": "Archivo base no encontrado"}

    # Guardar la base actual en un archivo
    config_path = os.path.join(BASE_DIR, "base_actual.txt")
    colors_path = os.path.join(BASE_DIR, "base_colors.txt")
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
    config_path = os.path.join(BASE_DIR, "base_actual.txt")
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
    colors_path = os.path.join(BASE_DIR, "base_colors.txt")
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
    colors_path = os.path.join(BASE_DIR, "base_colors.txt")
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

@app.post("/api/save_billing")
async def save_billing(
    request: Request,
    emisor_nombre: str = Form(...),
    emisor_cedula: str = Form(...),
    emisor_telefono: str = Form(...),
    emisor_email: str = Form(...),
    emisor_ciudad: str = Form(...),
    cuenta_bancolombia: str = Form(...),
    nequi_daviplata: str = Form(...),
    nota_pago: str = Form(...),
    firma: str = Form(...),
    user: str = Depends(auth.login_required)
):
    success = services.save_billing_data(
        emisor_nombre, emisor_cedula, emisor_telefono, emisor_email, emisor_ciudad,
        cuenta_bancolombia, nequi_daviplata, nota_pago, firma
    )
    if success:
        return {"success": True, "message": "Datos de facturación guardados correctamente"}
    else:
        return {"success": False, "message": "Error al guardar los datos"}

@app.get("/api/get_billing")
async def get_billing(request: Request, user: str = Depends(auth.login_required)):
    billing_data = services.get_billing_data()
    return billing_data
