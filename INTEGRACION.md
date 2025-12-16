# Integración Frontend-Backend CobraFlow

## Arquitectura del Proyecto

Este proyecto consiste en **DOS aplicaciones separadas**:

1. **Frontend React** (`app-react-frontend/`) - Landing page promocional
   - Puerto desarrollo: `http://localhost:8080` o `http://localhost:5173`
   - Propósito: Mostrar información del producto y redirigir a la aplicación

2. **Backend FastAPI** (`app-fastapi-backend/`) - Aplicación completa
   - Puerto: `http://localhost:8000`
   - Incluye: API, webapp con dashboard, generación de PDFs
   - Propósito: Aplicación funcional con todas las características

## Resumen de Cambios

El frontend ahora redirige correctamente al backend donde los usuarios pueden usar la aplicación completa con todas sus funcionalidades.

## Cambios Realizados

### Backend (app-fastapi-backend)

1. **Configuración de CORS** ([main.py:17-29](app-fastapi-backend/main.py#L17-L29))
   - Agregado middleware CORS para permitir requests desde:
     - `http://localhost:5173` (desarrollo local Vite)
     - `http://localhost:3000` (alternativa desarrollo)
     - `https://cobraflow.co` (producción)
     - `https://www.cobraflow.co` (producción con www)

2. **Nuevo Endpoint: `/api/crear-cuenta-simple/`** ([main.py:90-124](app-fastapi-backend/main.py#L90-L124))
   - No requiere clientes pre-registrados en `clientes.json`
   - Acepta el nombre del cliente directamente
   - Genera ID temporal para el cliente
   - Retorna el PDF generado

### Frontend (app-react-frontend)

1. **Componente Hero** ([Hero.tsx:6-9](app-react-frontend/src/components/Hero.tsx#L6-L9))
   - Botón "Probar Gratis Ahora" redirige a `${VITE_API_URL}/dashboard`

2. **Componente FinalCTA** ([FinalCTA.tsx:5-8](app-react-frontend/src/components/FinalCTA.tsx#L5-L8))
   - Botón redirige a `${VITE_API_URL}/dashboard`

3. **Componente InvoiceGenerator** ([InvoiceGenerator.tsx:66-69](app-react-frontend/src/components/InvoiceGenerator.tsx#L66-L69))
   - Botón "Generar" redirige a `${VITE_API_URL}/dashboard`

4. **Variable de entorno** ([.env:3](app-react-frontend/.env#L3))
   - `VITE_API_URL=http://localhost:8000` (desarrollo)
   - En producción se configurará según el deployment

## Configuración para Desarrollo Local

### Backend

1. Navega a la carpeta del backend:
```bash
cd app-fastapi-backend
```

2. Activa el entorno virtual:
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. Instala dependencias (si no están instaladas):
```bash
pip install -r requirements.txt
```

4. Inicia el servidor:
```bash
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

El backend estará disponible en: `http://localhost:8000`

### Frontend

1. Navega a la carpeta del frontend:
```bash
cd app-react-frontend
```

2. Instala dependencias (si no están instaladas):
```bash
npm install
```

3. Verifica el archivo `.env`:
```env
VITE_API_URL=http://localhost:8000
```

4. Inicia el servidor de desarrollo:
```bash
npm run dev
```

El frontend estará disponible en: `http://localhost:5173` (o el puerto que Vite asigne)

**Nota:** Si tu frontend corre en el puerto 8080, el archivo debe estar correcto.

## Configuración para Producción

### Opción 1: Nginx como Proxy Reverso (Recomendado)

Configuración de Nginx para servir frontend y backend:

```nginx
server {
    listen 80;
    server_name cobraflow.co www.cobraflow.co;

    # Frontend (React build)
    location / {
        root /var/www/cobraflow/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # Backend API
    location /api/ {
        proxy_pass http://localhost:8000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Backend crear-cuenta
    location /crear-cuenta/ {
        proxy_pass http://localhost:8000/crear-cuenta/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Backend docs (opcional)
    location /docs {
        proxy_pass http://localhost:8000/docs;
        proxy_set_header Host $host;
    }
}
```

### Pasos de Despliegue:

1. **Build del Frontend:**
```bash
cd app-react-frontend
npm run build
# Los archivos estarán en: dist/
```

2. **Configurar `.env` para producción:**
```env
VITE_API_URL=/api
```

3. **Backend con Gunicorn:**
```bash
cd app-fastapi-backend
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

4. **Configurar Systemd para auto-inicio (Linux):**

Crear archivo `/etc/systemd/system/cobraflow-backend.service`:
```ini
[Unit]
Description=CobraFlow Backend
After=network.target

[Service]
Type=notify
User=www-data
WorkingDirectory=/var/www/cobraflow/backend
Environment="PATH=/var/www/cobraflow/backend/venv/bin"
ExecStart=/var/www/cobraflow/backend/venv/bin/gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

[Install]
WantedBy=multi-user.target
```

Habilitar y iniciar:
```bash
sudo systemctl enable cobraflow-backend
sudo systemctl start cobraflow-backend
```

### Opción 2: Depliegue Separado

1. **Frontend en Vercel/Netlify:**
   - Conecta el repositorio
   - Build command: `npm run build`
   - Output directory: `dist`
   - Variables de entorno: `VITE_API_URL=https://api.cobraflow.co`

2. **Backend en VPS/Railway/Render:**
   - Puerto: 8000
   - Start command: `uvicorn main:app --host 0.0.0.0 --port 8000`
   - Actualizar CORS en `main.py` con la URL del frontend

## Flujo de Usuario Final

1. Usuario visita el **Frontend** en `http://localhost:8080` o `https://cobraflow.co` (landing page promocional)
2. Ve información del producto, beneficios, testimonios, etc.
3. Hace clic en **"Probar Gratis Ahora"**
4. Es redirigido al **Backend** en `http://localhost:8000/dashboard` (o producción)
5. Si no está logueado, ve la página de login
6. Ingresa credenciales demo:
   - Email: `demo@dtgrowthpartners.com`
   - Password: `demo123`
7. Accede al **Dashboard** con todas las funcionalidades:
   - Agregar clientes
   - Agregar servicios
   - Generar cuentas de cobro
   - Ver historial
   - Personalizar plantillas
8. Usa la aplicación completa para generar PDFs profesionales

## Endpoints Disponibles

### Backend

- `GET /` - Mensaje de bienvenida
- `GET /docs` - Documentación interactiva de la API
- `POST /crear-cuenta/` - Endpoint original (requiere cliente en clientes.json)
- `POST /api/crear-cuenta-simple/` - **Nuevo endpoint** (no requiere cliente previo)
- `GET /login` - Login de la webapp (requiere credenciales demo)
- `GET /dashboard` - Dashboard de la webapp (requiere autenticación)

### Frontend

- `/` - Landing page (promocional)
- Todos los botones CTA redirigen al backend

## Notas Importantes

1. **Archivos Generados:** Los PDFs se guardan en `app-fastapi-backend/creadas/`
2. **Base del PDF:** El diseño se controla desde `base_actual.txt` y `base_colors.txt`
3. **Datos del Emisor:** Están hardcoded en `generador.py` (líneas 57-63)
4. **Webapp Independiente:** La webapp en `/dashboard` sigue funcionando con login demo
5. **Sin Límites:** El nuevo flujo no tiene límite de cuentas generadas

## Solución de Problemas

### Error CORS
- Verificar que las URLs en `main.py` incluyan el origen del frontend
- En desarrollo, asegurarse que el backend esté en puerto 8000

### PDF no se descarga
- Verificar que la carpeta `creadas/` exista y tenga permisos de escritura
- Revisar logs del backend para errores en la generación

### Frontend no conecta con Backend
- Verificar variable `VITE_API_URL` en `.env`
- Asegurarse que el backend esté corriendo
- Verificar CORS en la consola del navegador

## Próximos Pasos Sugeridos

1. Agregar validación de email para contacto
2. Implementar límite de uso con localStorage
3. Agregar Google Analytics o similar
4. Implementar sistema de usuarios (opcional)
5. Agregar plantillas de PDF personalizables
6. Implementar envío por email del PDF generado
