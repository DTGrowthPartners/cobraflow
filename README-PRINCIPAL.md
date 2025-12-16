# CobraFlow - Generador de Cuentas de Cobro 💰

Sistema completo para generar cuentas de cobro profesionales en PDF.

## 🏗️ Arquitectura

Este proyecto está dividido en **DOS aplicaciones independientes**:

### 1. Frontend React (Landing Page)
- **Ubicación:** `app-react-frontend/`
- **Puerto:** `http://localhost:8080` o `http://localhost:5173`
- **Función:** Landing page promocional que muestra información del producto

### 2. Backend FastAPI (Aplicación Principal)
- **Ubicación:** `app-fastapi-backend/`
- **Puerto:** `http://localhost:8000`
- **Función:** Aplicación completa con dashboard, API REST, y generación de PDFs

```
┌──────────────────────────┐
│   FRONTEND (React)       │
│   Landing Page           │
│   localhost:8080         │
│                          │
│  [Probar Gratis Ahora]   │ ──────────┐
└──────────────────────────┘           │
                                       │ Redirige a
                                       │
                                       ▼
┌──────────────────────────┐
│   BACKEND (FastAPI)      │
│   Aplicación Completa    │
│   localhost:8000         │
│                          │
│  • Dashboard             │
│  • Generación de PDFs    │
│  • Gestión de Clientes   │
│  • API REST              │
└──────────────────────────┘
```

## 🚀 Inicio Rápido

### Paso 1: Iniciar el Backend

```bash
cd app-fastapi-backend

# Activar entorno virtual
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Instalar dependencias (primera vez)
pip install -r requirements.txt

# Iniciar servidor
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**✅ Backend listo en:** http://localhost:8000

### Paso 2: Iniciar el Frontend

```bash
cd app-react-frontend

# Instalar dependencias (primera vez)
npm install

# Verificar .env
# Debe contener: VITE_API_URL=http://localhost:8000

# Iniciar servidor de desarrollo
npm run dev
```

**✅ Frontend listo en:** http://localhost:5173 (o 8080)

## 🔐 Credenciales de Acceso

Para acceder al dashboard del backend:

- **Email:** `demo@dtgrowthpartners.com`
- **Password:** `demo123`

## 📖 Flujo de Usuario

```
1. Usuario entra al FRONTEND
   └─→ http://localhost:8080

2. Ve la landing page con:
   ├─ Hero con descripción del producto
   ├─ Beneficios
   ├─ Cómo funciona
   └─ Testimonios

3. Click en "Probar Gratis Ahora"
   └─→ Redirige a http://localhost:8000/dashboard

4. Si no está logueado:
   └─→ Página de login
       └─→ Ingresa credenciales demo

5. Accede al DASHBOARD con:
   ├─ Gestión de clientes
   ├─ Gestión de servicios
   ├─ Generación de cuentas de cobro
   ├─ Historial de documentos
   └─ Personalización de plantillas
```

## 📝 Generar una Cuenta de Cobro

### Método 1: Dashboard (Interfaz Gráfica)

1. Accede a http://localhost:8000/login
2. Login con credenciales demo
3. En el dashboard:
   - Agrega un cliente (nickname, nombre completo, NIT, dirección)
   - Opcionalmente, agrega servicios predefinidos
   - Genera cuenta seleccionando:
     - Cliente
     - Servicios (descripción, cantidad, precio unitario)
     - Concepto general
4. Descarga el PDF generado

### Método 2: API REST (Endpoint Simplificado)

```bash
curl -X POST "http://localhost:8000/api/crear-cuenta-simple/" \
  -H "Content-Type: application/json" \
  -d '{
    "nickname_cliente": "María García",
    "valor": 1500000,
    "servicios": [
      {
        "descripcion": "Desarrollo de landing page",
        "cantidad": 1,
        "precio_unitario": 800000
      },
      {
        "descripcion": "Configuración de dominio",
        "cantidad": 1,
        "precio_unitario": 200000
      },
      {
        "descripcion": "Hosting por 1 año",
        "cantidad": 12,
        "precio_unitario": 41666.67
      }
    ],
    "concepto": "Servicios de desarrollo web",
    "fecha": "16/12/2024",
    "servicio_proyecto": "Proyecto Web Corporativo"
  }'
```

Este endpoint:
- ✅ NO requiere cliente pre-registrado
- ✅ Genera ID temporal automáticamente
- ✅ Retorna PDF listo para descargar

## 🎨 Características

### Backend
- ✅ 6 plantillas de diseño diferentes
- ✅ Personalización de colores por plantilla
- ✅ Gestión completa de clientes (CRUD)
- ✅ Gestión de servicios predefinidos
- ✅ Historial de cuentas generadas
- ✅ Eliminación individual y masiva de documentos
- ✅ API REST documentada (Swagger/OpenAPI)
- ✅ Autenticación con sesiones

### Frontend
- ✅ Landing page responsive
- ✅ Diseño moderno con TailwindCSS
- ✅ Componentes reutilizables
- ✅ Animaciones suaves
- ✅ Optimizado para SEO

## 📂 Estructura del Proyecto

```
cobraflow/
│
├── app-react-frontend/              # Landing Page
│   ├── src/
│   │   ├── components/
│   │   │   ├── Hero.tsx            # Sección principal
│   │   │   ├── Benefits.tsx        # Beneficios
│   │   │   ├── HowItWorks.tsx      # Cómo funciona
│   │   │   ├── Testimonials.tsx    # Testimonios
│   │   │   ├── FinalCTA.tsx        # Call to action final
│   │   │   └── ...
│   │   ├── pages/
│   │   │   ├── Index.tsx           # Página principal
│   │   │   └── NotFound.tsx        # 404
│   │   └── App.tsx                 # Router principal
│   ├── .env                         # Variables de entorno
│   └── package.json
│
├── app-fastapi-backend/             # Aplicación Principal
│   ├── webapp/
│   │   ├── app.py                  # FastAPI app + rutas web
│   │   ├── auth.py                 # Autenticación
│   │   ├── services.py             # Lógica de negocio
│   │   ├── templates/              # Plantillas Jinja2
│   │   │   ├── login.html
│   │   │   └── dashboard.html
│   │   └── static/                 # CSS, JS, imágenes
│   ├── main.py                      # API REST
│   ├── generador.py                # Generación de PDFs
│   ├── clientes.json               # Base de datos clientes
│   ├── servicios.json              # Servicios predefinidos
│   ├── creadas/                    # PDFs generados
│   ├── base*.jpg                   # Plantillas de diseño
│   ├── fuentes/                    # Fuentes tipográficas
│   └── requirements.txt
│
├── INTEGRACION.md                   # Guía completa de integración
└── README-PRINCIPAL.md              # Este archivo
```

## 🔧 Configuración Detallada

### Variables de Entorno

**Frontend** (`.env`):
```env
# Desarrollo local
VITE_API_URL=http://localhost:8000

# Producción
VITE_API_URL=https://api.cobraflow.co
```

### Endpoints Disponibles

**Backend API:**
- `GET /` - Mensaje de bienvenida
- `GET /docs` - Documentación interactiva (Swagger UI)
- `POST /crear-cuenta/` - Endpoint original (requiere cliente en clientes.json)
- `POST /api/crear-cuenta-simple/` - Endpoint sin cliente previo (NUEVO)
- `GET /login` - Página de login
- `POST /login` - Procesar login
- `GET /dashboard` - Dashboard principal (requiere auth)
- `POST /dashboard/generate` - Generar cuenta desde dashboard
- `POST /api/add_client` - Agregar cliente
- `POST /api/add_service` - Agregar servicio
- `GET /api/get_clients` - Listar clientes
- `GET /api/get_services` - Listar servicios
- Y más...

## 🚢 Despliegue a Producción

Ver [INTEGRACION.md](INTEGRACION.md) para guía completa de deployment con:
- Configuración de Nginx como proxy reverso
- Deploy con Gunicorn
- Configuración de Systemd service
- SSL/HTTPS con Let's Encrypt
- Variables de entorno de producción

## 🐛 Solución de Problemas

### El botón "Probar Gratis" no funciona

**Causa:** El backend no está corriendo o la URL está mal configurada

**Solución:**
```bash
# 1. Verifica que el backend esté corriendo
# Debe ver: "Application startup complete"

# 2. Verifica el .env del frontend
cat app-react-frontend/.env
# Debe contener: VITE_API_URL=http://localhost:8000

# 3. Reinicia el frontend si cambiaste .env
cd app-react-frontend
npm run dev
```

### Error "Failed to fetch" o CORS

**Causa:** El backend no tiene configurado CORS para tu frontend

**Solución:** Ya está configurado en `main.py` líneas 18-29 para:
- `http://localhost:5173`
- `http://localhost:3000`
- `http://localhost:8080` (agregar si tu puerto es diferente)

### No puedo hacer login

**Credenciales correctas:**
- Email: `demo@dtgrowthpartners.com`
- Password: `demo123`

Verifica que el backend esté corriendo en puerto 8000.

### El PDF no se genera

**Posibles causas:**
1. La carpeta `creadas/` no existe → Se crea automáticamente
2. Permisos de escritura → Verifica permisos en la carpeta
3. Error en los datos → Revisa logs del backend

## 📚 Documentación Adicional

- **[INTEGRACION.md](INTEGRACION.md)** - Guía completa de integración y deployment
- **API Docs:** http://localhost:8000/docs (con backend corriendo)
- **OpenAPI Schema:** http://localhost:8000/openapi.json

## 🛠️ Stack Tecnológico

### Frontend
- React 18
- TypeScript
- Vite
- TailwindCSS
- Shadcn/ui components
- React Router DOM
- Sonner (toasts)

### Backend
- Python 3.8+
- FastAPI
- Uvicorn (ASGI server)
- ReportLab (generación PDF)
- Pillow (procesamiento imágenes)
- Jinja2 (templates HTML)
- Python Multipart (forms)

## 📞 Soporte

Para problemas o preguntas:
- Revisa [INTEGRACION.md](INTEGRACION.md)
- Consulta la documentación de la API: http://localhost:8000/docs
- Email: Dairo@dtgrowthpartners.com

## 📄 Licencia

Proyecto privado - © 2024 DT Growth Partners

---

**Desarrollado por DT Growth Partners**
🌐 https://cobraflow.co
