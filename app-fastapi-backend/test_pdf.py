from generador import generar_cuenta_de_cobro

# Datos de prueba
nombre_cliente = "Juan Pérez"
identificacion = "123456789"
servicios = [
    {"nombre_servicio": "Desarrollo web", "descripcion": "Creación de sitio web responsive", "cantidad": 1, "precio_unitario": 500000},
    {"nombre_servicio": "Mantenimiento", "descripcion": "Soporte mensual", "cantidad": 2, "precio_unitario": 100000}
]
concepto = "Desarrollo de software"
fecha = "2023-10-01"
servicio_proyecto = "Proyecto Web"

# Generar PDF
ruta_pdf = generar_cuenta_de_cobro(nombre_cliente, identificacion, servicios, concepto, fecha, servicio_proyecto)
print(f"PDF generado en: {ruta_pdf}")