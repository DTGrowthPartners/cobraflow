<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dairo Traslaviña - Factura</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            color: #333;
        }
        
        .invoice-header {
            width: 100%;
            max-width: 900px;
            margin: 0 auto;
        }
        
        .header-border {
            border-top: 4px solid #1a75a7;
            border-bottom: 4px solid #1a75a7;
            padding: 15px 0;
            margin-bottom: 20px;
        }
        
        .logo {
            max-width: 450px;
            margin-bottom: 20px;
        }
        
        .invoice-details {
            display: flex;
            justify-content: space-between;
        }
        
        .invoice-left {
            width: 35%;
        }
        
        .invoice-right {
            width: 60%;
        }
        
        .invoice-title {
            font-size: 32px;
            font-weight: 500;
            color: #444;
            margin: 0 0 10px 0;
            text-transform: uppercase;
            letter-spacing: normal;
            text-align: left;
        }
        
        .client-info {
            margin-bottom: 15px;
        }
        
        .client-name {
            font-weight: bold;
            font-size: 16px;
            margin-bottom: 5px;
        }
        
        .client-address, .client-date {
            margin: 3px 0;
        }
        
        .contact-info {
            color: #1a75a7;
            font-weight: bold;
            font-size: 16px;
            margin-bottom: 5px;
        }
        
        .location {
            color: #666;
        }
        
        .project-info p {
            margin: 5px 0;
        }
        
        .project-title, .project-description {
            font-weight: bold;
        }

        /* Estilos para la tabla de inventario */
        article {
            max-width: 900px;
            margin: 0 auto;
            padding: 20px 0;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
        }
        
        table th, table td {
            padding: 10px;
            text-align: left;
        }
        
        table.inventory th {
            background-color: #f2f2f2;
            border-bottom: 1px solid #ddd;
        }
        
        table.inventory td {
            border-bottom: 1px solid #eee;
        }
        
        table.inventory select {
            width: 100%;
            padding: 5px;
        }
        
        table.inventory input {
            width: 90%;
            padding: 5px;
            border: 1px solid #ddd;
        }
        
        .cut {
            cursor: pointer;
            color: #f44336;
            font-weight: bold;
            text-decoration: none;
            margin-right: 5px;
        }
        
        .add {
            display: block;
            text-align: center;
            padding: 10px;
            background-color: #1a75a7;
            color: white;
            cursor: pointer;
            font-weight: bold;
            margin: 10px 0;
        }
        
        table.balance {
            float: right;
            width: 36%;
            margin-top: 20px;
        }
        
        table.balance th {
            width: 50%;
        }
        
        /* Nueva sección para las notas y métodos de pago */
        .footer-section {
            display: flex;
            justify-content: space-between;
            max-width: 900px;
            margin: 0 auto;
            clear: both;
            padding-top: 20px;
        }
        
        .payment-notes {
            width: 48%;
        }
        
        .payment-methods {
            width: 48%;
        }
        
        .bancos {
            max-width: 120px;
            height: auto;
        }
        
        aside {
            max-width: 900px;
            margin: 0 auto;
            padding-top: 20px;
            clear: both;
        }
    </style>
</head>
<body>
    <div class="invoice-header">
        <div class="header-border">
            <img src="http://dairotraslavina.com/wp-content/uploads/2025/03/da_logo-dairo-copia.png" alt="Dairo Traslaviña Logo" class="logo">
            
            <div class="invoice-details">
                <div class="invoice-left">
                    <h1 class="invoice-title">Cuenta de <br>Cobro</h1>
                    <div class="contact-info">3007189383</div>
                    <div class="contact-info">Dairotras@gmail.com</div>
                    <div class="location">Cartagena, Colombia</div>
                </div>
                
                <div class="invoice-right">
                    <div class="client-info">
                        <div class="client-name">MOTOS TOP</div>
                        <div class="client-address">Cl. 31 #52 90,</div>
                        <div class="client-address">Progreso, Cartagena</div>
                        <div class="client-date">Fecha: 5/05/25</div>
                    </div>
                    
                    <div class="project-info">
                        <p><span class="project-title">Título del proyecto:</span> Gestión y Optimización de Campañas Publicitarias para Motos Top</p>
                        <p><span class="project-description">Descripción del proyecto:</span> Cobro por servicios prestados de gestión y optimización de campañas publicitarias en línea para Motos Top, así como comisiones derivadas de la inversión en pauta publicitaria del 15 al 30 de Abril.</p>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <article>
        <table class="inventory">
            <thead>
                <tr>
                    <th><span>Item</span></th>
                    <th><span>Precio</span></th>
                    <th><span>Cantidad</span></th>
                    <th><span>Total</span></th>
                </tr>
            </thead>
            <tbody id="invoice-items">
                <tr>
                    <td>
                        <a class="cut" onclick="removeRow(this)">-</a>
                        <select name="servicios">
                            <option value="PUBLICIDAD ONLINE">Publicidad Online</option>
                            <option value="DESARROLLO TIENDAS ONLINE">Desarrollo de Tiendas Online (E-commerce)</option>
                            <option value="OPTIMIZACION TIENDAS">Optimización de Tiendas Físicas</option>
                            <option value="AUDITORIA MARKETING">Auditoría de Marketing Digital</option>
                            <option value="CONSULTORIA CRECIMIENTO">Consultoría en Estrategias de Crecimiento</option>
                            <option value="PLAN DIGITALIZACION">Plan Integral de Digitalización</option>
                        </select>
                    </td>
                    <td><span data-prefix>$</span><input type="text" class="price" value="0" onchange="calculateRow(this)" onkeyup="calculateRow(this)"></td>
                    <td><input type="text" class="quantity" value="1" min="1" onchange="calculateRow(this)" onkeyup="calculateRow(this)"></td>
                    <td><span data-prefix>$</span><span class="row-total">0</span></td>
                </tr>
            </tbody>
        </table>
        <a class="add" onclick="addRow()">+</a>
        <table class="balance">
            <tr>
                <th><span>Subtotal</span></th>
                <td><span data-prefix>$</span><span id="subtotal">0</span></td>
            </tr>
            <tr>
                <th><span>Descuento</span></th>
                <td><span data-prefix>$</span><input type="number" id="discount" value="0" onchange="calculateTotal()"></td>
            </tr>
            <tr>
                <th><span>Total a pagar</span></th>
                <td><span data-prefix>$</span><span id="grand-total">0</span></td>
            </tr>
        </table>
    </article>
    
    <aside>
        <h1 style="font-size:15px"><span contenteditable>Notas adicionales <br></span></h1>
    </aside>
  
    <div class="footer-section">
        <div class="payment-notes">
            <p class="infotext" contenteditable style="font-size:13px">
                Páguese a:<br>
                Nombre: Dairo Traslaviña<br>
                Cédula: 1143397563<br>
                • Se solicita que el pago sea realizado a la mayor brevedad posible.<br>
            </p>
        </div>
        
        <div class="payment-methods">
            <table style="font-size:11px" width="100%">
                <tbody>
                    <tr>
                        <td width="180"><strong>Bancolombia</strong></td>
                        <td width="180"><strong>Nequi</strong></td>
                    </tr>
                    <tr>
                        <td>Ahorros: <strong>788 4170 7710</strong></td>
                        <td>3007189383</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>

    <!-- Script personalizado para la factura -->
    <script>
        // Función para formatear números con separador de miles
        function formatNumber(number) {
            return number.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
        }
        
        // Función para calcular el total de una fila
        function calculateRow(element) {
            const row = element.closest('tr');
            const price = parseFloat(row.querySelector('.price').value.replace(/\./g, '')) || 0;
            const quantity = parseFloat(row.querySelector('.quantity').value.replace(/\./g, '')) || 0;
            const total = price * quantity;
            
            // Formatear con separador de miles
            if (element.classList.contains('quantity')) {
                element.value = formatNumber(quantity);
            }
            if (element.classList.contains('price')) {
                element.value = formatNumber(price);
            }
            
            row.querySelector('.row-total').textContent = formatNumber(total);
            calculateTotal();
        }
        
        // Función para calcular el total general
        function calculateTotal() {
            let subtotal = 0;
            document.querySelectorAll('.row-total').forEach(function(element) {
                subtotal += parseFloat(element.textContent.replace(/\./g, '')) || 0;
            });
            
            const discount = parseFloat(document.getElementById('discount').value.replace(/\./g, '')) || 0;
            const grandTotal = subtotal - discount;
            
            document.getElementById('subtotal').textContent = formatNumber(subtotal);
            document.getElementById('grand-total').textContent = formatNumber(grandTotal);
            
            // Aplicar formato al descuento
            document.getElementById('discount').value = formatNumber(discount);
        }
        
        // Función para agregar una nueva fila
        function addRow() {
            const tbody = document.getElementById('invoice-items');
            const template = tbody.querySelector('tr').cloneNode(true);
            
            // Resetear valores
            template.querySelector('.price').value = '0';
            template.querySelector('.quantity').value = '1';
            template.querySelector('.row-total').textContent = '0';
            
            tbody.appendChild(template);
            calculateTotal();
        }
        
        // Función para eliminar una fila
        function removeRow(element) {
            const tbody = document.getElementById('invoice-items');
            if (tbody.querySelectorAll('tr').length > 1) {
                element.closest('tr').remove();
                calculateTotal();
            } else {
                alert('Debe haber al menos una fila en la factura.');
            }
        }
        
        // Inicializar cálculos
        document.addEventListener('DOMContentLoaded', function() {
            calculateTotal();
        });
    </script>
    
    <!-- Script original adaptado -->
    <script>
/* Shivving (IE8 is not supported, but at least it won't look as awful)
/* ========================================================================== */

(function (document) {
	var
	head = document.head = document.getElementsByTagName('head')[0] || document.documentElement,
	elements = 'article aside audio bdi canvas data datalist details figcaption figure footer header hgroup mark meter nav output picture progress section summary time video x'.split(' '),
	elementsLength = elements.length,
	elementsIndex = 0,
	element;

	while (elementsIndex < elementsLength) {
		element = document.createElement(elements[++elementsIndex]);
	}

	element.innerHTML = 'x<style>' +
		'article,aside,details,figcaption,figure,footer,header,hgroup,nav,section{display:block}' +
		'audio[controls],canvas,video{display:inline-block}' +
		'[hidden],audio{display:none}' +
		'mark{background:#FF0;color:#000}' +
	'</style>';

	return head.insertBefore(element.lastChild, head.firstChild);
})(document);

/* Prototyping
/* ========================================================================== */

(function (window, ElementPrototype, ArrayPrototype, polyfill) {
	function NodeList() { [polyfill] }
	NodeList.prototype.length = ArrayPrototype.length;

	ElementPrototype.matchesSelector = ElementPrototype.matchesSelector ||
	ElementPrototype.mozMatchesSelector ||
	ElementPrototype.msMatchesSelector ||
	ElementPrototype.oMatchesSelector ||
	ElementPrototype.webkitMatchesSelector ||
	function matchesSelector(selector) {
		return ArrayPrototype.indexOf.call(this.parentNode.querySelectorAll(selector), this) > -1;
	};

	ElementPrototype.ancestorQuerySelectorAll = ElementPrototype.ancestorQuerySelectorAll ||
	ElementPrototype.mozAncestorQuerySelectorAll ||
	ElementPrototype.msAncestorQuerySelectorAll ||
	ElementPrototype.oAncestorQuerySelectorAll ||
	ElementPrototype.webkitAncestorQuerySelectorAll ||
	function ancestorQuerySelectorAll(selector) {
		for (var cite = this, newNodeList = new NodeList; cite = cite.parentElement;) {
			if (cite.matchesSelector(selector)) ArrayPrototype.push.call(newNodeList, cite);
		}

		return newNodeList;
	};

	ElementPrototype.ancestorQuerySelector = ElementPrototype.ancestorQuerySelector ||
	ElementPrototype.mozAncestorQuerySelector ||
	ElementPrototype.msAncestorQuerySelector ||
	ElementPrototype.oAncestorQuerySelector ||
	ElementPrototype.webkitAncestorQuerySelector ||
	function ancestorQuerySelector(selector) {
		return this.ancestorQuerySelectorAll(selector)[0] || null;
	};
})(this, Element.prototype, Array.prototype);
    </script>
</body>
</html>