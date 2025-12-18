import os
from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from generador import generar_cuenta_de_cobro
from datetime import datetime
import json
from fastapi import Request
from fastapi.responses import HTMLResponse
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

# Plantillas: webapp/templates/*.html
templates = Jinja2Templates(directory=str(BASE_DIR / "webapp" / "templates"))

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

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})