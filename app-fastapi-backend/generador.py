import os
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def get_top_colors(image, exclude_white=True, top=2):
    colors = image.getcolors(image.size[0] * image.size[1])
    if not colors:
        return []
    # Sort by count descending
    colors.sort(key=lambda x: x[0], reverse=True)
    filtered = []
    for count, color in colors:
        if exclude_white and color == (255, 255, 255):
            continue
        filtered.append(color)
        if len(filtered) >= top:
            break
    return filtered

def generar_cuenta_de_cobro(nombre_cliente: str, identificacion: str, servicios: list, concepto: str, fecha: str, servicio_proyecto: str = None, nombre_empresa: str = "", fuente_seleccionada: str = "HelveticaNeue.ttf") -> str:
    """
    Genera una cuenta de cobro en formato PDF con una tabla detallada de servicios.

    Args:
        nombre_cliente: El nombre del cliente.
        identificacion: La identificación del cliente.
        servicios: Una lista de diccionarios con 'nombre_servicio', 'descripcion', 'cantidad', 'precio_unitario'.
        concepto: El concepto general de la cuenta de cobro.
        fecha: La fecha de la cuenta de cobro.
        servicio_proyecto: Nombres de los servicios/proyectos separados por comas.

    Returns:
        La ruta del archivo PDF generado.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # --- GENERACIÓN DEL PDF ---
    numero_cuenta = datetime.now().strftime("%Y%m%d%H%M%S")

    # --- DATOS DEL EMISOR ---
    emisor_nombre = "Dairo Tralasviña"
    emisor_cedula = "1143397563"
    emisor_telefono = "+57 3007189383"
    emisor_email = "Dairo@dtgrowthpartners.com"
    emisor_ciudad = "Cartagena, Colombia"
    cuenta_bancolombia = "78841707710"
    nequi = "+57 3007189383"

    # --- REGISTRAR FUENTE SELECCIONADA ---
    fuentes_dir = os.path.join(script_dir, 'fuentes')
    fuente_path = os.path.join(fuentes_dir, fuente_seleccionada)
    if os.path.exists(fuente_path):
        # Registrar la fuente seleccionada
        font_name = fuente_seleccionada.replace('.ttf', '').replace('.otf', '')
        pdfmetrics.registerFont(TTFont(font_name, fuente_path))
        # Usar la fuente seleccionada para todo el texto
        normal_font = font_name
        bold_font = font_name  # Por simplicidad, usar la misma fuente para bold
        italic_font = font_name
    else:
        # Fallback a fuentes por defecto
        if os.path.isdir(fuentes_dir):
            mapa_fuentes = {'HN-Normal': 'HelveticaNeueLight.ttf', 'HN-Bold': 'HelveticaNeueBold.ttf', 'HN-Italic': 'HelveticaNeueItalic.ttf'}
            for nombre, archivo in mapa_fuentes.items():
                ruta_fuente = os.path.join(fuentes_dir, archivo)
                if os.path.exists(ruta_fuente):
                    pdfmetrics.registerFont(TTFont(nombre, ruta_fuente))
            pdfmetrics.registerFontFamily('HelveticaNeue', normal='HN-Normal', bold='HN-Bold', italic='HN-Italic')
        normal_font = 'HN-Normal'
        bold_font = 'HN-Bold'
        italic_font = 'HN-Italic'

    # --- RUTA IMAGEN BASE ---
    archivo_base = None
    config_path = os.path.join(script_dir, "base_actual.txt")
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            base_name = f.read().strip()
        path_completo = os.path.join(script_dir, base_name)
        if os.path.exists(path_completo):
            archivo_base = path_completo
    if not archivo_base:
        # Fallback a base.jpg
        path_completo = os.path.join(script_dir, "base.jpg")
        if os.path.exists(path_completo):
            archivo_base = path_completo

    # Determinar colores para textos según la base
    original_base_name = base_name
    base_name = os.path.basename(archivo_base) if archivo_base else 'base.jpg'
    primary_color_hex = "#005F99"  # Color por defecto
    header_color_rgb = (0/255, 95/255, 153/255)  # Color por defecto para header

    if base_name != 'base.jpg':
        colors_path = os.path.join(script_dir, "base_colors.txt")
        if os.path.exists(colors_path):
            with open(colors_path, "r") as f:
                lines = f.readlines()
                if len(lines) >= 1:
                    primary_color_hex = lines[0].strip()
                    primary_rgb = hex_to_rgb(primary_color_hex)
                    header_color_rgb = (primary_rgb[0]/255, primary_rgb[1]/255, primary_rgb[2]/255)

    # Aplicar colores a la imagen si PIL está disponible y la base lo requiere
    if archivo_base and PIL_AVAILABLE:
        apply_colors = False
        if base_name == 'Base2.jpg':
            apply_primary = True
            apply_secondary = False
        elif base_name in ['Base3.jpg', 'Base4.jpg', 'Base5.jpg', 'Base6.jpg']:
            apply_primary = True
            apply_secondary = True
        else:
            apply_primary = False
            apply_secondary = False

        if apply_primary or apply_secondary:
            colors_path = os.path.join(script_dir, "base_colors.txt")
            if os.path.exists(colors_path):
                with open(colors_path, "r") as f:
                    lines = f.readlines()
                    if len(lines) >= 1:
                        primary_hex = lines[0].strip()
                        primary_rgb = hex_to_rgb(primary_hex)
                        secondary_rgb = None
                        if len(lines) >= 2 and apply_secondary:
                            secondary_hex = lines[1].strip()
                            secondary_rgb = hex_to_rgb(secondary_hex)
                        # Abrir imagen y detectar colores
                        img = Image.open(archivo_base).convert('RGB')
                        top_colors = get_top_colors(img, exclude_white=True, top=2)
                        # Crear mapping
                        color_mapping = {}
                        if apply_primary and len(top_colors) >= 1:
                            color_mapping[top_colors[0]] = primary_rgb
                        if apply_secondary and secondary_rgb and len(top_colors) >= 2:
                            color_mapping[top_colors[1]] = secondary_rgb
                        # Aplicar mapping con tolerance
                        pixels = img.load()
                        tolerance = 100
                        for x in range(img.size[0]):
                            for y in range(img.size[1]):
                                for old_color, new_color in color_mapping.items():
                                    if all(abs(pixels[x, y][k] - old_color[k]) <= tolerance for k in range(3)):
                                        pixels[x, y] = new_color
                                        break
                        # Guardar en temp
                        temp_path = os.path.join(script_dir, 'creadas', 'temp_base.jpg')
                        img.save(temp_path)
                        archivo_base = temp_path

    nombre_archivo = f"cuenta_cobro_{nombre_cliente.replace(' ', '_')}_{numero_cuenta}.pdf"
    os.makedirs(os.path.join(script_dir, 'creadas'), exist_ok=True)
    ruta_salida = os.path.join(script_dir, 'creadas', nombre_archivo)

    c = canvas.Canvas(ruta_salida, pagesize=letter)
    width, height = letter

    if archivo_base:
        c.drawImage(archivo_base, 0, 0, width=width, height=height, preserveAspectRatio=False)

    # Posiciones dinámicas según la base
    base_name = os.path.basename(archivo_base) if archivo_base else 'base.jpg'
    positions = {
        'base.jpg': {
            'title_y': height - 120,
            'info_y': height - 160,
            'cliente_y': height - 240,
            'table_y': height - 350,
        },
        'Base2.jpg': {
            'title_y': height - 120,
            'info_y': height - 180,
            'cliente_y': height - 260,
            'table_y': height - 390,
        },
        'Base3.jpg': {
            'title_y': height - 130,
            'info_y': height - 180,
            'cliente_y': height - 240,
            'table_y': height - 345,
        },
        'Base4.jpg': {
            'title_y': height - 135,
            'info_y': height - 170,
            'cliente_y': height - 240,
            'table_y': height - 350,
        },
        'Base5.jpg': {
            'title_y': height - 210,
            'info_y': height - 260,
            'cliente_y': height - 320,
            'table_y': height - 410,
        },
        'Base6.jpg': {
            'title_y': height - 120,
            'info_y': height - 180,
            'cliente_y': height - 260,
            'table_y': height - 390,
        },
    }
    pos = positions.get(original_base_name, positions['base.jpg'])

    margen_izquierdo = 95 if original_base_name == 'Base6.jpg' else 40

    # Mostrar nombre de empresa como título encima si existe y base >=2
    if nombre_empresa and original_base_name != 'base.jpg':
        c.setFont(bold_font, 16)
        c.setFillColor(colors.HexColor(primary_color_hex))
        if original_base_name in ['Base2.jpg', 'Base3.jpg']:
            c.drawString(margen_izquierdo, pos['title_y'] + 50, nombre_empresa.upper())
        else:
            c.drawCentredString(width / 2.0, pos['title_y'] + 50, nombre_empresa.upper())

    if original_base_name in ['Base2.jpg', 'Base3.jpg']:
        c.setFont(bold_font, 22)
        c.setFillColor(colors.HexColor(primary_color_hex))
        c.drawString(margen_izquierdo, pos['title_y'], f"CUENTA DE COBRO N.° {numero_cuenta}")
    elif original_base_name == 'Base6.jpg':
        c.setFont(bold_font, 18)
        c.setFillColor(colors.HexColor(primary_color_hex))
        c.drawString(margen_izquierdo, pos['title_y'], f"CUENTA DE COBRO N.° {numero_cuenta}")
    else:
        c.setFont(bold_font, 22)
        c.setFillColor(colors.HexColor(primary_color_hex))
        c.drawCentredString(width / 2.0, pos['title_y'], f"CUENTA DE COBRO N.° {numero_cuenta}")

    y = pos['info_y']
    c.setFont(normal_font, 9)
    c.setFillColor(colors.HexColor(primary_color_hex))
    c.drawString(margen_izquierdo, y, emisor_telefono)
    y -= 15
    c.drawString(margen_izquierdo, y, emisor_email)
    y -= 15
    c.setFillColor(colors.HexColor(primary_color_hex))
    c.drawString(margen_izquierdo, y, emisor_ciudad)

    y = pos['cliente_y']
    c.setFont(bold_font, 9)
    c.setFillColor(colors.black)

    label_cliente = "Cliente:"
    c.drawString(margen_izquierdo, y, label_cliente)
    label_width = c.stringWidth(label_cliente, bold_font, 9)
    c.setFont(normal_font, 9)
    c.drawString(margen_izquierdo + label_width + 2, y, nombre_cliente)

    y -= 15
    c.setFont(bold_font, 9)
    label_id = "Identificación:"
    c.drawString(margen_izquierdo, y, label_id)
    label_width = c.stringWidth(label_id, bold_font, 9)
    c.setFont(normal_font, 9)
    c.drawString(margen_izquierdo + label_width + 2, y, identificacion)

    y -= 15
    c.setFont(bold_font, 9)
    label_fecha = "Fecha:"
    c.drawString(margen_izquierdo, y, label_fecha)
    label_width = c.stringWidth(label_fecha, bold_font, 9)
    c.setFont(normal_font, 9)
    c.drawString(margen_izquierdo + label_width + 2, y, fecha)

    if original_base_name == 'Base3.jpg':
        y -= 30
    elif original_base_name == 'Base4.jpg':
        y -= 30
    else:
        y -= 30
    c.setFont(bold_font, 9)
    label_concepto = "Servicio / Proyecto:"
    c.drawString(margen_izquierdo, y, label_concepto)
    label_width = c.stringWidth(label_concepto, bold_font, 9)
    c.setFont(normal_font, 9)

    # Usar servicio_proyecto si está disponible, sino usar concepto
    texto_servicio = servicio_proyecto if servicio_proyecto else concepto
    c.drawString(margen_izquierdo + label_width + 2, y, texto_servicio)

    # --- TABLA DE SERVICIOS ---
    col_widths = [250, 30, 120, 100]
    if original_base_name == 'Base3.jpg':
        row_height = 30
    else:
        row_height = 25
    table_y_start = pos['table_y']
    header_color = colors.Color(red=header_color_rgb[0], green=header_color_rgb[1], blue=header_color_rgb[2])

    c.setFillColor(header_color)
    c.rect(margen_izquierdo, table_y_start, sum(col_widths), row_height, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont(bold_font, 9)
    headers = ["Descripción", "Cantidad", "Precio Unitario", "Total"]
    for i, header in enumerate(headers):
        c.drawCentredString(margen_izquierdo + sum(col_widths[:i]) + col_widths[i]/2, table_y_start + 6, header)

    current_y, total_general = table_y_start, 0
    c.setFont(normal_font, 9)
    c.setFillColor(colors.black)

    styles = getSampleStyleSheet()

    for servicio in servicios:
        current_y -= row_height
        total_servicio = servicio['precio_unitario'] * servicio['cantidad']
        total_general += total_servicio
        c.setStrokeColorRGB(0.8, 0.8, 0.8)
        c.grid([margen_izquierdo, margen_izquierdo + col_widths[0], margen_izquierdo + sum(col_widths[:2]), margen_izquierdo + sum(col_widths[:3]), margen_izquierdo + sum(col_widths)], [current_y, current_y + row_height])

        # Descripción con wrapping
        desc_style = ParagraphStyle('desc', parent=styles['Normal'], fontName=normal_font, fontSize=9, leading=12)
        desc_p = Paragraph(servicio['descripcion'], desc_style)
        desc_width = col_widths[0] - 20
        w, h = desc_p.wrap(desc_width, row_height - 4)  # leave margin
        desc_y = current_y + 2 + (row_height - 4 - h) / 2
        desc_p.drawOn(c, margen_izquierdo + 10, desc_y)

        text_y = current_y + (row_height / 2) - 3
        c.drawCentredString(margen_izquierdo + col_widths[0] + col_widths[1]/2, text_y, str(servicio['cantidad']))
        c.drawRightString(margen_izquierdo + sum(col_widths[:3]) - 10, text_y, f"$ {servicio['precio_unitario']:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        c.drawRightString(margen_izquierdo + sum(col_widths) - 10, text_y, f"$ {total_servicio:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

    current_y -= row_height
    c.grid([margen_izquierdo, margen_izquierdo + sum(col_widths)], [current_y, current_y + row_height])
    c.setFont(bold_font, 10)
    c.drawString(margen_izquierdo + col_widths[0] + col_widths[1] + 10, current_y + 6, "Total General")
    c.drawRightString(margen_izquierdo + sum(col_widths) - 10, current_y + 6, f"$ {total_general:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    if original_base_name == 'Base3.jpg':
        y = current_y - 30
    elif original_base_name == 'Base4.jpg':
        y = current_y - 35
    else:
        y = current_y - 15

    # --- PÁGUESE A ---
    c.setFont(bold_font, 9)
    c.drawString(margen_izquierdo, y, "Páguese A:")
    y -= 15
    c.setFont(normal_font, 9)
    c.drawString(margen_izquierdo, y, f"Nombre: {emisor_nombre}")
    y -= 12
    c.drawString(margen_izquierdo, y, f"Cédula: {emisor_cedula}")
    y -= 12
    c.drawString(margen_izquierdo, y, f"Cuenta de ahorros Bancolombia: {cuenta_bancolombia}")
    y -= 12
    c.drawString(margen_izquierdo, y, f"Nequi / Daviplata: {nequi}")

    y -= 30
    # --- NOTA ---
    c.setFont(bold_font, 9)
    c.drawString(margen_izquierdo, y, "Nota:")
    nota_width = c.stringWidth("Nota:", bold_font, 9)
    c.setFont(normal_font, 9)
    c.drawString(margen_izquierdo + nota_width + 2, y, " Se solicita que el pago sea realizado a la mayor brevedad posible")

    y -= 30
    c.setFont(normal_font, 9)
    c.drawString(margen_izquierdo, y, "Atentamente,")
    y -= 15
    c.drawString(margen_izquierdo, y, "Dairo Tralasviña,")

    c.save()

    # Limpiar archivo temporal si existe
    if archivo_base and 'temp_base.jpg' in archivo_base:
        try:
            os.remove(archivo_base)
        except OSError:
            pass  # Ignorar si no se puede eliminar

    return ruta_salida