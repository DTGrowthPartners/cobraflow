# 🔗 Documentación de Integración - CobraFlow

## 📋 Descripción General

Este documento describe cómo se integran los dos proyectos de CobraFlow:

1. **Landing Page en React** (`app-react-frontend`): Muestra las características del producto y redirige a la aplicación
2. **Aplicación Web FastAPI** (`app-fastapi-backend`): Aplicación principal para generar cuentas de cobro en PDF

## 🏗️ Arquitectura de Integración

```
┌─────────────────────────────┐         ┌──────────────────────────────┐
│  Landing Page (React)       │         │  App FastAPI (Backend)       │
│  Puerto: 5173               │         │  Puerto: 8000                │
│                             │         │                              │
│  - Muestra características  │─────────▶│  - Login (demo/demo123)     │
│  - Botones CTA redirigen    │         │  - Dashboard                 │
│  - Información del producto │         │  - Generación de PDFs        │
└─────────────────────────────┘         └──────────────────────────────┘
```

## 📝 Cambios Realizados

### 1. Backend (FastAPI) - `app-fastapi-backend/webapp/app.py`

#### CORS Configurado
Se agregó el middleware CORS para permitir requests desde React:

```python
from fastapi.middleware.cors import CORSMiddleware

FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL, "http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 2. Frontend (React)

#### Variables de Entorno - `.env`
Creado archivo con la URL del backend:

```env
VITE_API_URL=http://localhost:8000
```

#### Componentes Modificados

**Hero.tsx** - Botón principal redirige al login:
```typescript
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const redirectToApp = () => {
  window.location.href = `${API_URL}/login`;
};
```

**FinalCTA.tsx** - Llamado a la acción final:
```typescript
const redirectToApp = () => {
  window.location.href = `${API_URL}/login`;
};
```

**InvoiceGenerator.tsx** - Generador de demostración redirige a la app:
```typescript
const generateInvoice = () => {
  window.location.href = `${API_URL}/login`;
};
```

## 🚀 Cómo Ejecutar en Desarrollo

### Paso 1: Configurar Variables de Entorno

#### Frontend (React)
```bash
cd app-react-frontend
cp .env.example .env
# Edita .env si es necesario
```

#### Backend (FastAPI)
```bash
cd app-fastapi-backend
cp .env.example .env
# Edita .env si es necesario
```

### Paso 2: Instalar Dependencias

#### Frontend (React)
```bash
cd app-react-frontend
npm install
# O si usas bun:
bun install
```

#### Backend (FastAPI)
```bash
cd app-fastapi-backend
pip install -r requirements.txt
```

### Paso 3: Ejecutar Ambos Proyectos

#### Terminal 1 - Backend (FastAPI)
```bash
cd app-fastapi-backend
python -m webapp.app
```
El backend estará disponible en: `http://localhost:8000`

#### Terminal 2 - Frontend (React)
```bash
cd app-react-frontend
npm run dev
# O con bun:
bun run dev
```
El frontend estará disponible en: `http://localhost:5173`

### Paso 4: Probar la Integración

1. Abre tu navegador en `http://localhost:5173`
2. Navega por la landing page
3. Haz clic en "Probar Gratis Ahora" o "Generar cuenta de cobro"
4. Serás redirigido a `http://localhost:8000/login`
5. Usa las credenciales de demo:
   - **Email:** demo@dtgrowthpartners.com
   - **Password:** demo123
6. Accederás al dashboard donde puedes generar cuentas de cobro reales

## 🔐 Credenciales de Demo

Para acceder a la aplicación FastAPI:
- **Email:** `demo@dtgrowthpartners.com`
- **Password:** `demo123`

## 📦 Estructura de Archivos

```
cobraflow/
├── app-react-frontend/              # Landing page en React
│   ├── src/
│   │   ├── components/
│   │   │   ├── Hero.tsx            # ✅ Modificado - Redirección al login
│   │   │   ├── FinalCTA.tsx        # ✅ Modificado - Redirección al login
│   │   │   └── InvoiceGenerator.tsx # ✅ Modificado - Redirección al login
│   │   └── ...
│   ├── .env                         # ✅ Nuevo - Variables de entorno
│   ├── .env.example                 # ✅ Nuevo - Ejemplo de variables
│   └── package.json
│
├── app-fastapi-backend/             # Aplicación FastAPI
│   ├── webapp/
│   │   ├── app.py                  # ✅ Modificado - CORS configurado
│   │   ├── templates/
│   │   │   ├── login.html          # Página de login
│   │   │   └── dashboard.html      # Dashboard principal
│   │   └── ...
│   ├── .env.example                # ✅ Nuevo - Ejemplo de variables
│   └── requirements.txt
│
└── README_INTEGRACION.md           # ✅ Este archivo
```

## 🌐 Despliegue en Producción

### Variables de Entorno en Producción

#### Frontend
```env
VITE_API_URL=https://api.tudominio.com
```

#### Backend
```env
FRONTEND_URL=https://www.tudominio.com
SECRET_KEY=una-clave-secreta-muy-segura-generada-aleatoriamente
```

### Recomendaciones de Despliegue

#### Frontend (React)
- **Vercel** (recomendado): Deploy automático desde GitHub
- **Netlify**: Alternativa popular
- **GitHub Pages**: Para proyectos estáticos

Configuración en Vercel/Netlify:
```bash
# Build command
npm run build

# Output directory
dist

# Environment variables
VITE_API_URL=https://api.tudominio.com
```

#### Backend (FastAPI)
- **Railway** (recomendado): Deploy sencillo para apps Python
- **Render**: Alternativa gratuita
- **Heroku**: Opción clásica
- **VPS** (DigitalOcean, AWS): Mayor control

Ejemplo con Uvicorn:
```bash
uvicorn webapp.app:app --host 0.0.0.0 --port 8000
```

## 🧪 Testing de la Integración

### Checklist de Pruebas

- [ ] Landing page carga correctamente en `http://localhost:5173`
- [ ] Botón "Probar Gratis Ahora" redirige a `/login` del backend
- [ ] Botón "Ver cómo funciona" hace scroll en la landing
- [ ] Login funciona con credenciales de demo
- [ ] Dashboard carga después del login exitoso
- [ ] Se puede generar una cuenta de cobro PDF
- [ ] No hay errores de CORS en la consola del navegador

### Comandos de Verificación

```bash
# Verificar que el backend esté corriendo
curl http://localhost:8000/

# Verificar que el frontend esté corriendo
curl http://localhost:5173/
```

## ⚠️ Troubleshooting

### Error: CORS policy blocking requests
**Solución:** Verifica que las URLs en el archivo `.env` del backend coincidan con la URL del frontend.

### Error: Cannot connect to backend
**Solución:** Asegúrate de que el backend esté corriendo en el puerto 8000.

### Error: Environment variable not found
**Solución:** Verifica que el archivo `.env` exista y tenga las variables correctas.

### Redirección no funciona
**Solución:** Verifica que `VITE_API_URL` esté configurado correctamente en `.env` del frontend.

## 📞 Soporte

Si tienes problemas con la integración:
1. Verifica que ambos proyectos estén corriendo
2. Revisa la consola del navegador para errores
3. Verifica que las variables de entorno estén configuradas correctamente
4. Asegúrate de que no haya conflictos de puertos

## 🎯 Flujo de Usuario

1. Usuario visita la landing page → `http://localhost:5173`
2. Usuario explora las características del producto
3. Usuario hace clic en "Probar Gratis Ahora"
4. Usuario es redirigido a → `http://localhost:8000/login`
5. Usuario ingresa credenciales demo
6. Usuario accede al dashboard
7. Usuario genera cuentas de cobro PDF

## 📊 Resumen de Cambios

| Archivo | Tipo de Cambio | Descripción |
|---------|----------------|-------------|
| `app-fastapi-backend/webapp/app.py` | Modificado | Se agregó configuración CORS |
| `app-react-frontend/src/components/Hero.tsx` | Modificado | Redirección al login |
| `app-react-frontend/src/components/FinalCTA.tsx` | Modificado | Redirección al login |
| `app-react-frontend/src/components/InvoiceGenerator.tsx` | Modificado | Redirección al login |
| `app-react-frontend/.env` | Nuevo | Variables de entorno |
| `app-react-frontend/.env.example` | Nuevo | Ejemplo de variables |
| `app-fastapi-backend/.env.example` | Nuevo | Ejemplo de variables |
| `README_INTEGRACION.md` | Nuevo | Esta documentación |

---

**Última actualización:** 2025-12-15
**Versión:** 1.0.0
