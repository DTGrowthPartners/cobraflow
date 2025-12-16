# Proyecto: Generador de Cuentas de Cobro (API + Demo Web)

Este proyecto contiene una API de Python para generar cuentas de cobro en formato PDF y una aplicación web de demostración para interactuar con ella.

## Descripción

La funcionalidad principal se divide en dos partes:

1.  **API (`main.py`):** Un endpoint de FastAPI que recibe datos y genera un PDF de cuenta de cobro.
2.  **Aplicación Web (`webapp/`):** Una interfaz web construida con FastAPI y Jinja2 que sirve como una demostración comercial del generador de cuentas.

## Características de la Demo Web

-   **Pantalla de Login:** Acceso a la aplicación con credenciales de demostración.
-   **Dashboard Interactivo:**
    -   Seleccionar un cliente de una lista precargada.
    -   Rellenar un formulario para generar una nueva cuenta de cobro.
    -   Previsualizar el PDF generado directamente en la web.
    -   Ver un historial de todas las cuentas generadas anteriormente.
-   **Diseño Simple y Limpio:** Interfaz de usuario sencilla y profesional para la demostración.

---

## Cómo Empezar

Sigue estos pasos para instalar las dependencias y ejecutar la aplicación web de demostración.

### 1. Prerrequisitos

-   Python 3.10+
-   `pip` (manejador de paquetes de Python)

### 2. Instalación

1.  **Clona el repositorio (si aún no lo has hecho):**
    ```bash
    git clone <url-del-repositorio>
    cd <nombre-del-repositorio>
    ```

2.  **Crea un entorno virtual (recomendado):**
    ```bash
    python -m venv .venv
    ```
    Activa el entorno virtual:
    -   **Windows:**
        ```bash
        .venv\Scripts\activate
        ```
    -   **macOS/Linux:**
        ```bash
        source .venv/bin/activate
        ```

3.  **Instala las dependencias:**
    Todas las dependencias necesarias están listadas en `requirements.txt`.
    ```bash
    pip install -r requirements.txt
    ```

### 3. Ejecutar la Aplicación Web

Para iniciar la aplicación web de demostración, ejecuta el siguiente comando desde el **directorio raíz del proyecto** (`PROYECTOS/cuentas_de_cobro_app_web`):

```bash
uvicorn webapp.app:app --reload --host 0.0.0.0 --port 8000
```

-   `uvicorn`: Es el servidor ASGI que ejecutará la aplicación FastAPI.
-   `webapp.app:app`: Le dice a Uvicorn dónde encontrar la instancia de la aplicación FastAPI (el objeto `app` dentro del archivo `webapp/app.py`).
-   `--reload`: Reinicia el servidor automáticamente cada vez que detecta un cambio en el código. Ideal para desarrollo.

### 4. Acceder a la Demo

Una vez que el servidor esté en funcionamiento, abre tu navegador web y ve a la siguiente URL:

**[http://localhost:8000/login](http://localhost:8000/login)**

Usa las siguientes credenciales de prueba para ingresar:

-   **Email:** `demo@dtgrowthpartners.com`
-   **Password:** `demo123`

---

## Estructura del Proyecto

```
.
├── main.py                 # API original (aún funcional)
├── generador.py            # Lógica principal para crear el PDF
├── clientes.json           # Base de datos de clientes en formato JSON
├── creadas/                # Carpeta donde se guardan los PDFs generados
├── webapp/
│   ├── app.py              # Punto de entrada de la aplicación web (FastAPI)
│   ├── auth.py             # Lógica de autenticación simple
│   ├── services.py         # Conecta la UI con la lógica de negocio
│   ├── static/
│   │   └── styles.css      # Hoja de estilos
│   └── templates/
│       ├── base.html       # Plantilla base
│       ├── login.html      # Página de login
│       └── dashboard.html  # Dashboard principal
├── requirements.txt        # Dependencias del proyecto
└── README.md               # Este archivo
```
