import json
import os
from typing import List, Dict, Any, Optional

# Importar la lógica de negocio principal desde los otros módulos
# Necesitamos ajustar el path para que Python encuentre los módulos del directorio raíz
import sys
# Añade el directorio raíz del proyecto al path de Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from generador import generar_cuenta_de_cobro

# --- CONSTANTES ---
CLIENTES_FILE = "clientes.json"
SERVICIOS_FILE = "servicios.json"
CREADAS_DIR = "creadas"

def list_clients() -> List[Dict[str, Any]]:
    """
    Lee y devuelve la lista de clientes desde clientes.json.
    """
    try:
        # La ruta es relativa al directorio raíz del proyecto
        with open(CLIENTES_FILE, "r", encoding="utf-8") as f:
            clients_data = json.load(f)
            # Convertir el diccionario a una lista de diccionarios
            client_list = [{"nickname": key, **value} for key, value in clients_data.items()]
        return client_list
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

def get_client_by_nickname(nickname: str) -> Optional[Dict[str, Any]]:
    """
    Obtiene los datos de un cliente específico por su nickname.
    """
    try:
        with open(CLIENTES_FILE, "r", encoding="utf-8") as f:
            clientes = json.load(f)
        return clientes.get(nickname)
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def generate_invoice_service(
    nickname_cliente: str,
    servicios: list,
    concepto: str,
    fecha: str,
    servicio_proyecto: str,
    nombre_empresa: str = "",
    fuente_seleccionada: str = "HelveticaNeue.ttf",
    emisor_nombre: str = "Dairo Tralasviña",
    emisor_cedula: str = "1143397563",
    emisor_telefono: str = "+57 3007189383",
    emisor_email: str = "Dairo@dtgrowthpartners.com",
    emisor_ciudad: str = "Cartagena, Colombia",
    cuenta_bancolombia: str = "78841707710",
    nequi_daviplata: str = "+57 3007189383",
    nota_pago: str = "Se solicita que el pago sea realizado a la mayor brevedad posible",
    firma: str = "Dairo Tralasviña,"
) -> str:
    """
    Llama a la función principal para generar el PDF de la cuenta de cobro.
    
    Retorna:
        La ruta del archivo PDF generado.
    """
    client_data = get_client_by_nickname(nickname_cliente)
    if not client_data:
        raise ValueError(f"Cliente '{nickname_cliente}' no encontrado.")
    
    # Llamada a la función importada del módulo generador
    pdf_path = generar_cuenta_de_cobro(
        nombre_cliente=client_data['nombre_completo'],
        identificacion=client_data['nit'],
        servicios=servicios,
        concepto=concepto,
        fecha=fecha,
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
        firma=firma
    )
    
    return pdf_path

def list_generated_invoices() -> List[Dict[str, str]]:
    """
    Escanea el directorio 'creadas' y devuelve una lista de las facturas generadas.
    """
    invoices = []
    if not os.path.isdir(CREADAS_DIR):
        return invoices

    for filename in sorted(os.listdir(CREADAS_DIR), reverse=True):
        if filename.endswith(".pdf"):
            # Extraer información del nombre del archivo si es posible (ej: 'cuenta_cobro_Cliente_X_20231027103000.pdf')
            parts = filename.replace('.pdf', '').split('_')
            client_name = parts[2] if len(parts) > 2 else "Desconocido"
            date_str = parts[-1] if len(parts) > 3 else "Sin fecha"

            invoices.append({
                "filename": filename,
                "client_name": client_name.replace('_', ' '),
                "date_str": date_str,
                "url": f"/creadas/{filename}" # URL para acceder al archivo
            })
    return invoices

def list_services() -> List[Dict[str, Any]]:
    """
    Lee y devuelve la lista de servicios predefinidos desde servicios.json.
    """
    try:
        with open(SERVICIOS_FILE, "r", encoding="utf-8") as f:
            services_data = json.load(f)
            return services_data.get("servicios", [])
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

def add_new_service(nombre: str, descripcion: str, categoria: str) -> bool:
    """
    Añade un nuevo servicio al archivo servicios.json.
    """
    try:
        # Leer servicios existentes
        if os.path.exists(SERVICIOS_FILE):
            with open(SERVICIOS_FILE, "r", encoding="utf-8") as f:
                services_data = json.load(f)
        else:
            services_data = {"servicios": []}

        # Añadir nuevo servicio
        new_service = {
            "nombre": nombre,
            "descripcion": descripcion,
            "categoria": categoria
        }
        services_data["servicios"].append(new_service)

        # Guardar cambios
        with open(SERVICIOS_FILE, "w", encoding="utf-8") as f:
            json.dump(services_data, f, indent=2, ensure_ascii=False)

        return True
    except Exception as e:
        print(f"Error al añadir servicio: {e}")
        return False

def add_new_client(nickname: str, nombre_completo: str, direccion: str, nit: str) -> bool:
    """
    Añade un nuevo cliente al archivo clientes.json.
    """
    try:
        # Leer clientes existentes
        if os.path.exists(CLIENTES_FILE):
            with open(CLIENTES_FILE, "r", encoding="utf-8") as f:
                clients_data = json.load(f)
        else:
            clients_data = {}

        # Añadir nuevo cliente
        clients_data[nickname] = {
            "nombre_completo": nombre_completo,
            "direccion": direccion,
            "nit": nit
        }

        # Guardar cambios
        with open(CLIENTES_FILE, "w", encoding="utf-8") as f:
            json.dump(clients_data, f, indent=2, ensure_ascii=False)

        return True
    except Exception as e:
        print(f"Error al añadir cliente: {e}")
        return False

def delete_invoice_file(filename: str) -> bool:
    """
    Elimina un archivo PDF generado del directorio 'creadas'.
    """
    try:
        file_path = os.path.join(CREADAS_DIR, filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False
    except Exception as e:
        print(f"Error al eliminar archivo: {e}")
        return False

def delete_multiple_invoices(filenames: List[str]) -> Dict[str, bool]:
    """
    Elimina múltiples archivos PDF generados del directorio 'creadas'.
    Retorna un diccionario con el resultado para cada archivo.
    """
    results = {}
    for filename in filenames:
        results[filename] = delete_invoice_file(filename)
    return results

def edit_client(nickname: str, nombre_completo: str, direccion: str, nit: str) -> bool:
    """
    Edita los datos de un cliente existente.
    """
    try:
        # Leer clientes existentes
        if not os.path.exists(CLIENTES_FILE):
            return False

        with open(CLIENTES_FILE, "r", encoding="utf-8") as f:
            clients_data = json.load(f)

        if nickname not in clients_data:
            return False

        # Actualizar cliente
        clients_data[nickname] = {
            "nombre_completo": nombre_completo,
            "direccion": direccion,
            "nit": nit
        }

        # Guardar cambios
        with open(CLIENTES_FILE, "w", encoding="utf-8") as f:
            json.dump(clients_data, f, indent=2, ensure_ascii=False)

        return True
    except Exception as e:
        print(f"Error al editar cliente: {e}")
        return False

def delete_client(nickname: str) -> bool:
    """
    Elimina un cliente del archivo clientes.json.
    """
    try:
        # Leer clientes existentes
        if not os.path.exists(CLIENTES_FILE):
            return False

        with open(CLIENTES_FILE, "r", encoding="utf-8") as f:
            clients_data = json.load(f)

        if nickname not in clients_data:
            return False

        # Eliminar cliente
        del clients_data[nickname]

        # Guardar cambios
        with open(CLIENTES_FILE, "w", encoding="utf-8") as f:
            json.dump(clients_data, f, indent=2, ensure_ascii=False)

        return True
    except Exception as e:
        print(f"Error al eliminar cliente: {e}")
        return False

def edit_service(index: int, nombre: str, descripcion: str, categoria: str) -> bool:
    """
    Edita un servicio existente por su índice en la lista.
    """
    try:
        # Leer servicios existentes
        if not os.path.exists(SERVICIOS_FILE):
            return False

        with open(SERVICIOS_FILE, "r", encoding="utf-8") as f:
            services_data = json.load(f)

        services_list = services_data.get("servicios", [])
        if index < 0 or index >= len(services_list):
            return False

        # Actualizar servicio
        services_list[index] = {
            "nombre": nombre,
            "descripcion": descripcion,
            "categoria": categoria
        }

        # Guardar cambios
        with open(SERVICIOS_FILE, "w", encoding="utf-8") as f:
            json.dump(services_data, f, indent=2, ensure_ascii=False)

        return True
    except Exception as e:
        print(f"Error al editar servicio: {e}")
        return False

def delete_service(index: int) -> bool:
    """
    Elimina un servicio de la lista por su índice.
    """
    try:
        # Leer servicios existentes
        if not os.path.exists(SERVICIOS_FILE):
            return False

        with open(SERVICIOS_FILE, "r", encoding="utf-8") as f:
            services_data = json.load(f)

        services_list = services_data.get("servicios", [])
        if index < 0 or index >= len(services_list):
            return False

        # Eliminar servicio
        del services_list[index]

        # Guardar cambios
        with open(SERVICIOS_FILE, "w", encoding="utf-8") as f:
            json.dump(services_data, f, indent=2, ensure_ascii=False)

        return True
    except Exception as e:
        print(f"Error al eliminar servicio: {e}")
        return False

def list_fonts() -> List[Dict[str, str]]:
    """
    Lista las fuentes disponibles en la carpeta fuentes.
    """
    fonts = []
    fuentes_dir = os.path.join(os.path.dirname(__file__), '..', 'fuentes')

    if os.path.exists(fuentes_dir):
        for filename in os.listdir(fuentes_dir):
            if filename.lower().endswith(('.ttf', '.otf')):
                # Extraer nombre de fuente del archivo
                name = filename.replace('.ttf', '').replace('.otf', '')
                # Crear un nombre legible
                display_name = name.replace('-', ' ').replace('_', ' ').title()
                fonts.append({
                    'filename': filename,
                    'name': display_name,
                    'path': f'/fuentes/{filename}'
                })

    # Ordenar alfabéticamente
    fonts.sort(key=lambda x: x['name'])
    return fonts

def save_billing_data(emisor_nombre: str, emisor_cedula: str, emisor_telefono: str, emisor_email: str, emisor_ciudad: str, cuenta_bancolombia: str, nequi_daviplata: str, nota_pago: str, firma: str) -> bool:
    """
    Guarda los datos de facturación en un archivo JSON.
    """
    try:
        billing_data = {
            "emisor_nombre": emisor_nombre,
            "emisor_cedula": emisor_cedula,
            "emisor_telefono": emisor_telefono,
            "emisor_email": emisor_email,
            "emisor_ciudad": emisor_ciudad,
            "cuenta_bancolombia": cuenta_bancolombia,
            "nequi_daviplata": nequi_daviplata,
            "nota_pago": nota_pago,
            "firma": firma
        }

        billing_file = os.path.join(os.path.dirname(__file__), '..', 'billing_data.json')
        with open(billing_file, "w", encoding="utf-8") as f:
            json.dump(billing_data, f, indent=2, ensure_ascii=False)

        return True
    except Exception as e:
        print(f"Error al guardar datos de facturación: {e}")
        return False

def get_billing_data() -> Dict[str, str]:
    """
    Obtiene los datos de facturación desde el archivo JSON.
    """
    try:
        billing_file = os.path.join(os.path.dirname(__file__), '..', 'billing_data.json')
        if os.path.exists(billing_file):
            with open(billing_file, "r", encoding="utf-8") as f:
                return json.load(f)
        else:
            # Valores por defecto
            return {
                "emisor_nombre": "Dairo Tralasviña",
                "emisor_cedula": "1143397563",
                "emisor_telefono": "+57 3007189383",
                "emisor_email": "Dairo@dtgrowthpartners.com",
                "emisor_ciudad": "Cartagena, Colombia",
                "cuenta_bancolombia": "78841707710",
                "nequi_daviplata": "+57 3007189383",
                "nota_pago": "Se solicita que el pago sea realizado a la mayor brevedad posible",
                "firma": "Dairo Tralasviña,"
            }
    except Exception as e:
        print(f"Error al cargar datos de facturación: {e}")
        return {}