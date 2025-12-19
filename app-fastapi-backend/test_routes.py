#!/usr/bin/env python3
"""
Script para verificar que todas las rutas están registradas correctamente
"""

from main import app

print("=" * 60)
print("VERIFICACIÓN DE RUTAS DE COBRAFLOW")
print("=" * 60)

routes_by_path = {}
for route in app.routes:
    if hasattr(route, 'path') and hasattr(route, 'methods'):
        path = route.path
        methods = route.methods
        if path not in routes_by_path:
            routes_by_path[path] = []
        routes_by_path[path].extend(methods)

print("\nRutas Web:")
print("-" * 60)
web_routes = [
    "/",
    "/login",
    "/logout",
    "/dashboard",
    "/template-editor",
    "/dashboard/generate"
]

for path in web_routes:
    if path in routes_by_path:
        methods = ', '.join(sorted(routes_by_path[path]))
        print(f"[OK] {path:30} [{methods}]")
    else:
        print(f"[X]  {path:30} [NO ENCONTRADA]")

print("\nRutas API:")
print("-" * 60)
api_routes = [
    "/api/save_billing",
    "/api/get_billing",
    "/api/add_client",
    "/api/add_service",
    "/api/get_clients",
    "/api/get_services",
    "/api/set_base",
    "/api/get_base",
    "/api/set_colors",
    "/api/get_colors"
]

for path in api_routes:
    if path in routes_by_path:
        methods = ', '.join(sorted(routes_by_path[path]))
        print(f"[OK] {path:30} [{methods}]")
    else:
        print(f"[X]  {path:30} [NO ENCONTRADA]")

print("\n" + "=" * 60)
print(f"Total de rutas registradas: {len(routes_by_path)}")
print("=" * 60)

# Verificar archivo de plantilla
import os
template_path = os.path.join("webapp", "templates", "template_editor.html")
if os.path.exists(template_path):
    print(f"\n[OK] Archivo de plantilla existe: {template_path}")
    print(f"     Tamanio: {os.path.getsize(template_path)} bytes")
else:
    print(f"\n[X]  Archivo de plantilla NO existe: {template_path}")

print("\n" + "=" * 60)
print("NOTA: Para acceder a /template-editor debes:")
print("1. Iniciar sesión primero en /login")
print("2. La ruta requiere autenticación")
print("=" * 60)
