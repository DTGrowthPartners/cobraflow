# CONTEXTO DE LA TAREA

Tengo dos proyectos separados que necesito integrar:

1. *Landing Page en React* (Proyecto A)
   - Ubicación: [RUTA_DEL_PROYECTO_REACT]
   - Propósito: Promocionar y captar usuarios para la aplicación
   - Framework: React
   - Estado: Código completo y funcional

2. *Aplicación Web en fastapi* (Proyecto B)
   - Ubicación: [RUTA_DEL_PROYECTO_fastapi]
   - Propósito: Aplicación principal con funcionalidades backend
   - Framework: fastapi (Python)
   - Estado: Código completo y funcional

# OBJETIVO

Integrar ambos proyectos para que funcionen como un ecosistema unificado donde:
- La landing en React promocione y redirija a la app fastapi
- Ambos compartan autenticación/sesión de usuarios (si aplica)
- Se comuniquen mediante API REST

# TAREAS ESPECÍFICAS

## 1. ANÁLISIS INICIAL
- Examina la estructura de ambos proyectos
- Identifica los archivos principales de configuración
- Detecta si existe algún sistema de autenticación actual
- Lista las dependencias actuales de cada proyecto

## 2. CONFIGURACIÓN DE fastapi COMO API
- Habilita CORS en fastapi para aceptar requests desde React
- Crea/organiza las rutas API bajo el prefijo /api/
- Implementa manejo de errores consistente (JSON responses)
- Configura variables de entorno para URLs y secrets

## 3. CONFIGURACIÓN DE REACT PARA CONSUMIR API
- Crea un archivo de configuración para la URL base del API
- Implementa un servicio/módulo para las llamadas HTTP
- Configura axios o fetch con interceptors si es necesario
- Maneja tokens de autenticación en localStorage/cookies

## 4. INTEGRACIÓN DE AUTENTICACIÓN (Si aplica)
- Implementa JWT o sessions compartidas
- Crea endpoints de login/logout/registro en fastapi
- Conecta el formulario de React con estos endpoints
- Implementa protección de rutas en ambos lados

## 5. DESPLIEGUE Y CONFIGURACIÓN
- Proporciona instrucciones para deploy separado (desarrollo)
- Configura CORS con las URLs correctas según entorno
- Crea archivos .env.example para ambos proyectos
- Documenta las variables de entorno necesarias

# ENTREGABLES ESPERADOS

1. *Código modificado* en ambos proyectos con comentarios explicativos
2. *Archivo README_INTEGRACION.md* con:
   - Pasos de configuración
   - Variables de entorno requeridas
   - Comandos para correr ambos proyectos
   - Ejemplos de uso de la API
3. *Lista de cambios* realizados en cada proyecto
4. *Pruebas básicas* para verificar la integración

# RESTRICCIONES Y PREFERENCIAS

- Mantener la estructura actual de ambos proyectos lo más posible
- Usar buenas prácticas de seguridad (no hardcodear credenciales)
- Código limpio y bien comentado en español
- Priorizar soluciones simples y mantenibles

# INFORMACIÓN ADICIONAL

[Agrega aquí cualquier detalle específico sobre tus proyectos:]
- ¿La app fastapi ya tiene rutas API o solo vistas HTML?
- ¿Necesitas autenticación o solo redirección?
- ¿Qué funcionalidades específicas de fastapi debe consumir React?
- ¿URLs actuales de desarrollo de ambos proyectos?

# INSTRUCCIONES DE EJECUCIÓN

1. Primero analiza ambos proyectos completamente
2. Pregunta cualquier duda antes de hacer cambios
3. Implementa los cambios de forma incremental
4. Prueba cada integración antes de continuar
5. Documenta cada paso realizado