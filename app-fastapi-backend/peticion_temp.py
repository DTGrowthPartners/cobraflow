import requests
import json

# URL de tu VPS
url_api = "http://149.56.133.201:8000/crear-cuenta/"

datos_factura = {
    "nickname_cliente": "experiencia_cartagena",
    "valor": 2000000,  # ✅ Campo requerido - valor total de la factura
    "servicios": [
        {
            "descripcion": "Restante sitio web",
            "cantidad": 1,
            "precio_unitario": 1000000
        },
        {
            "descripcion": "Avance 50% ads",
            "cantidad": 1,
            "precio_unitario": 1000000
        }
    ],
    "concepto": "Servicios de desarrollo y marketing"
}

response = requests.post(url_api, json=datos_factura)

if response.status_code == 200:
    with open("cuenta_generada.pdf", "wb") as f:
        f.write(response.content)
    print("✅ PDF generado exitosamente: cuenta_generada.pdf")
else:
    print(f"❌ Error: {response.status_code}")
    print(response.json())