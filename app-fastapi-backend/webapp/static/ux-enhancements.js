// ===== COBRAFLOW UX ENHANCEMENTS =====
// Sistema de mejoras de experiencia de usuario para CobraFlow
// Implementa: Validación, Toasts, FAB, Modal de Confirmación, Tooltips

// ========== 1. TOAST NOTIFICATION SYSTEM ==========
const ToastSystem = {
    container: null,

    init() {
        if (!this.container) {
            this.container = document.createElement('div');
            this.container.className = 'toast-container';
            document.body.appendChild(this.container);
        }
    },

    show(options) {
        this.init();

        const {
            type = 'info', // success, error, warning, info
            title = '',
            message = '',
            duration = 5000,
            closable = true
        } = options;

        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;

        const icons = {
            success: '✅',
            error: '❌',
            warning: '⚠️',
            info: 'ℹ️'
        };

        toast.innerHTML = `
            <div class="toast-icon">${icons[type]}</div>
            <div class="toast-content">
                ${title ? `<div class="toast-title">${title}</div>` : ''}
                <div class="toast-message">${message}</div>
            </div>
            ${closable ? '<button class="toast-close">×</button>' : ''}
        `;

        this.container.appendChild(toast);

        if (closable) {
            toast.querySelector('.toast-close').addEventListener('click', () => {
                this.remove(toast);
            });
        }

        if (duration > 0) {
            setTimeout(() => this.remove(toast), duration);
        }

        return toast;
    },

    remove(toast) {
        toast.classList.add('toast-hiding');
        setTimeout(() => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        }, 300);
    },

    success(message, title = '¡Éxito!') {
        return this.show({ type: 'success', title, message });
    },

    error(message, title = 'Error') {
        return this.show({ type: 'error', title, message });
    },

    warning(message, title = 'Advertencia') {
        return this.show({ type: 'warning', title, message });
    },

    info(message, title = 'Información') {
        return this.show({ type: 'info', title, message });
    }
};

// ========== 2. VALIDATION SYSTEM ==========
const ValidationSystem = {
    // Reglas de validación por campo
    rules: {
        'client': {
            required: true,
            message: 'Debes seleccionar un cliente antes de continuar'
        },
        'servicio_descripcion_1': {
            required: true,
            message: 'La descripción del servicio es obligatoria'
        },
        'servicio_cantidad_1': {
            required: true,
            min: 1,
            message: 'La cantidad debe ser al menos 1'
        },
        'servicio_precio_1': {
            required: true,
            min: 0.01,
            message: 'El precio debe ser mayor a 0'
        },
        'tipo_operacion': {
            required: true,
            message: 'Debes seleccionar el tipo de operación'
        },
        'moneda': {
            required: true,
            message: 'Debes seleccionar la moneda'
        },
        'plazo_pago': {
            required: true,
            message: 'Debes seleccionar el plazo de pago'
        },
        'texto_legal': {
            required: true,
            minLength: 10,
            message: 'El texto legal debe tener al menos 10 caracteres'
        },
        'emisor-nombre-wizard': {
            required: true,
            message: 'El nombre del emisor es obligatorio'
        },
        'emisor-cedula-wizard': {
            required: true,
            message: 'La cédula/NIT del emisor es obligatoria'
        },
        'emisor-telefono-wizard': {
            required: true,
            message: 'El teléfono del emisor es obligatorio'
        },
        'emisor-email-wizard': {
            required: true,
            pattern: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
            message: 'Debes ingresar un email válido'
        },
        'emisor-banco-wizard': {
            required: true,
            message: 'Debes seleccionar un banco'
        },
        'emisor-numero-cuenta-wizard': {
            required: true,
            message: 'El número de cuenta es obligatorio'
        }
    },

    // Validar un campo individual
    validateField(fieldId) {
        const field = document.getElementById(fieldId);
        if (!field) return true;

        const rule = this.rules[fieldId];
        if (!rule) return true;

        const value = field.value.trim();
        const formGroup = field.closest('.form-group-wizard') || field.closest('.form-group');

        // Limpiar errores previos
        this.clearFieldError(fieldId);

        // Validar required
        if (rule.required && !value) {
            this.showFieldError(fieldId, rule.message);
            return false;
        }

        // Validar minLength
        if (rule.minLength && value.length < rule.minLength) {
            this.showFieldError(fieldId, rule.message);
            return false;
        }

        // Validar min (números)
        if (rule.min !== undefined && parseFloat(value) < rule.min) {
            this.showFieldError(fieldId, rule.message);
            return false;
        }

        // Validar pattern (regex)
        if (rule.pattern && !rule.pattern.test(value)) {
            this.showFieldError(fieldId, rule.message);
            return false;
        }

        return true;
    },

    // Mostrar error en un campo
    showFieldError(fieldId, message) {
        const field = document.getElementById(fieldId);
        if (!field) return;

        const formGroup = field.closest('.form-group-wizard') || field.closest('.form-group');
        if (!formGroup) return;

        formGroup.classList.add('has-error');

        // Crear mensaje de error si no existe
        let errorMsg = formGroup.querySelector('.error-message');
        if (!errorMsg) {
            errorMsg = document.createElement('div');
            errorMsg.className = 'error-message';
            field.parentNode.appendChild(errorMsg);
        }

        errorMsg.textContent = message;

        // Scroll al primer error
        if (document.querySelectorAll('.has-error').length === 1) {
            formGroup.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
    },

    // Limpiar error de un campo
    clearFieldError(fieldId) {
        const field = document.getElementById(fieldId);
        if (!field) return;

        const formGroup = field.closest('.form-group-wizard') || field.closest('.form-group');
        if (!formGroup) return;

        formGroup.classList.remove('has-error');

        const errorMsg = formGroup.querySelector('.error-message');
        if (errorMsg) {
            errorMsg.remove();
        }
    },

    // Validar todo el formulario
    validateForm() {
        let isValid = true;
        const errors = [];

        // Validar campos básicos
        const fieldsToValidate = [
            'client',
            'servicio_descripcion_1',
            'servicio_cantidad_1',
            'servicio_precio_1',
            'tipo_operacion',
            'moneda',
            'plazo_pago',
            'texto_legal',
            'emisor-nombre-wizard',
            'emisor-cedula-wizard',
            'emisor-telefono-wizard',
            'emisor-email-wizard',
            'emisor-banco-wizard',
            'emisor-numero-cuenta-wizard'
        ];

        fieldsToValidate.forEach(fieldId => {
            if (!this.validateField(fieldId)) {
                isValid = false;
                const rule = this.rules[fieldId];
                if (rule) {
                    errors.push(rule.message);
                }
            }
        });

        // Validar servicios adicionales
        let serviceNum = 2;
        while (document.querySelector(`[name="servicio_descripcion_${serviceNum}"]`)) {
            const descField = document.querySelector(`[name="servicio_descripcion_${serviceNum}"]`);
            const cantField = document.querySelector(`[name="servicio_cantidad_${serviceNum}"]`);
            const precioField = document.querySelector(`[name="servicio_precio_${serviceNum}"]`);

            if (descField && !descField.value.trim()) {
                this.showFieldError(descField.id || `servicio_descripcion_${serviceNum}`,
                    `La descripción del servicio ${serviceNum} es obligatoria`);
                isValid = false;
            }

            if (cantField && (!cantField.value || parseInt(cantField.value) < 1)) {
                isValid = false;
            }

            if (precioField && (!precioField.value || parseFloat(precioField.value) <= 0)) {
                isValid = false;
            }

            serviceNum++;
        }

        if (!isValid) {
            ToastSystem.error(
                `Se encontraron ${errors.length} errores. Por favor corrige los campos marcados en rojo.`,
                'Formulario incompleto'
            );
        }

        return isValid;
    },

    // Inicializar validación en tiempo real
    initLiveValidation() {
        Object.keys(this.rules).forEach(fieldId => {
            const field = document.getElementById(fieldId);
            if (field) {
                field.addEventListener('blur', () => {
                    this.validateField(fieldId);
                });

                field.addEventListener('input', () => {
                    if (field.closest('.form-group-wizard')?.classList.contains('has-error')) {
                        this.validateField(fieldId);
                    }
                });
            }
        });
    }
};

// ========== 3. CONFIRMATION MODAL ==========
const ConfirmationModal = {
    modal: null,

    init() {
        if (!this.modal) {
            this.modal = document.createElement('div');
            this.modal.id = 'confirm-generation-modal';
            this.modal.className = 'confirm-modal';
            document.body.appendChild(this.modal);
        }
    },

    show() {
        this.init();

        // Recopilar datos del formulario
        const data = this.collectFormData();

        this.modal.innerHTML = `
            <div class="confirm-modal-content">
                <div class="confirm-modal-header">
                    <div class="confirm-modal-icon">📄</div>
                    <h2 class="confirm-modal-title">Confirmar generación de cuenta de cobro</h2>
                </div>
                <div class="confirm-modal-body">
                    <p style="margin: 0 0 20px 0; color: var(--text-secondary); font-size: 14px;">
                        Verifica que toda la información sea correcta antes de generar el PDF
                    </p>
                    <div class="confirm-summary">
                        <div class="confirm-summary-row">
                            <span class="confirm-summary-label">Cliente</span>
                            <span class="confirm-summary-value">${data.cliente}</span>
                        </div>
                        <div class="confirm-summary-row">
                            <span class="confirm-summary-label">Servicio</span>
                            <span class="confirm-summary-value">${data.servicio}</span>
                        </div>
                        <div class="confirm-summary-row">
                            <span class="confirm-summary-label">Tipo de operación</span>
                            <span class="confirm-summary-value">${data.tipoOperacion}</span>
                        </div>
                        <div class="confirm-summary-row">
                            <span class="confirm-summary-label">Monto</span>
                            <span class="confirm-summary-value">${data.monto}</span>
                        </div>
                        ${data.retenciones ? `
                        <div class="confirm-summary-row">
                            <span class="confirm-summary-label">Retenciones</span>
                            <span class="confirm-summary-value">${data.retenciones}</span>
                        </div>
                        ` : ''}
                        <div class="confirm-summary-row">
                            <span class="confirm-summary-label">Total a recibir</span>
                            <span class="confirm-summary-value highlight">${data.total}</span>
                        </div>
                        <div class="confirm-summary-row">
                            <span class="confirm-summary-label">Plazo de pago</span>
                            <span class="confirm-summary-value">${data.plazo}</span>
                        </div>
                    </div>
                </div>
                <div class="confirm-modal-footer">
                    <button type="button" class="btn btn-secondary" onclick="ConfirmationModal.hide()">
                        Volver a editar
                    </button>
                    <button type="button" class="btn btn-primary" onclick="ConfirmationModal.confirm()">
                        ✓ Generar PDF
                    </button>
                </div>
            </div>
        `;

        this.modal.style.display = 'block';

        // Cerrar al hacer clic fuera
        this.modal.addEventListener('click', (e) => {
            if (e.target === this.modal) {
                this.hide();
            }
        });
    },

    hide() {
        if (this.modal) {
            this.modal.style.display = 'none';
        }
    },

    confirm() {
        this.hide();
        // Enviar el formulario
        const form = document.querySelector('.wizard-form');
        if (form) {
            ToastSystem.info('Generando cuenta de cobro...', 'Procesando');
            form.submit();
        }
    },

    collectFormData() {
        // Cliente
        const clienteNickname = document.getElementById('client')?.value || '';
        const cliente = allClients?.find(c => c.nickname === clienteNickname);
        const clienteNombre = cliente ? `${cliente.nombre_completo} (${cliente.nit})` : 'No seleccionado';

        // Servicio
        const servicioDesc = document.querySelector('[name="servicio_descripcion_1"]')?.value || '';
        const servicioCant = document.querySelector('[name="servicio_cantidad_1"]')?.value || '';
        const servicioPrecio = document.querySelector('[name="servicio_precio_1"]')?.value || '';
        const servicioText = `${servicioDesc} × ${servicioCant}`;

        // Tipo de operación
        const tipoOpSelect = document.getElementById('tipo_operacion');
        const tipoOperacion = tipoOpSelect ? tipoOpSelect.options[tipoOpSelect.selectedIndex]?.text : '';

        // Montos
        const montoText = document.getElementById('monto-numero-text')?.textContent || '';
        const totalText = document.getElementById('total-display')?.textContent || montoText;

        // Retenciones
        const retencionesDiv = document.getElementById('retenciones-detail');
        const retenciones = retencionesDiv && retencionesDiv.innerHTML.trim() ?
            retencionesDiv.textContent.trim() : '';

        // Plazo
        const plazoSelect = document.getElementById('plazo-pago');
        const plazo = plazoSelect ? plazoSelect.options[plazoSelect.selectedIndex]?.text : '';

        return {
            cliente: clienteNombre,
            servicio: servicioText,
            tipoOperacion,
            monto: montoText,
            retenciones,
            total: totalText,
            plazo
        };
    }
};

// ========== 4. CHARACTER COUNTER ==========
function initCharacterCounters() {
    const fields = [
        { id: 'emisor-nota-wizard', max: 500 },
        { id: 'texto-legal', max: 1000 }
    ];

    fields.forEach(({ id, max }) => {
        const field = document.getElementById(id);
        if (!field) return;

        // Crear contador
        const counter = document.createElement('div');
        counter.className = 'char-counter';
        counter.id = `${id}-counter`;
        counter.innerHTML = `
            <span class="char-count">0/${max}</span>
            <div class="char-progress-bar">
                <div class="char-progress-fill" style="width: 0%"></div>
            </div>
        `;

        field.parentNode.appendChild(counter);

        // Actualizar contador
        function updateCounter() {
            const length = field.value.length;
            const percentage = (length / max) * 100;
            const countSpan = counter.querySelector('.char-count');
            const progressFill = counter.querySelector('.char-progress-fill');

            countSpan.textContent = `${length}/${max}`;
            progressFill.style.width = `${Math.min(percentage, 100)}%`;

            // Cambiar estilos según el porcentaje
            counter.classList.remove('char-warning', 'char-error');
            progressFill.classList.remove('warning', 'error');

            if (percentage > 100) {
                counter.classList.add('char-error');
                progressFill.classList.add('error');
            } else if (percentage > 80) {
                counter.classList.add('char-warning');
                progressFill.classList.add('warning');
            }
        }

        field.addEventListener('input', updateCounter);
        updateCounter();
    });
}

// ========== 5. IMPROVED CLIENT SELECTION DISPLAY ==========
function enhanceClientSelection() {
    const originalSelectClient = window.selectClient;

    window.selectClient = function(nickname, nombre, nit) {
        // Llamar a la función original
        if (originalSelectClient) {
            originalSelectClient(nickname, nombre, nit);
        }

        // Mejorar la visualización
        const selectedDisplay = document.getElementById('selected-client-display');
        if (selectedDisplay) {
            selectedDisplay.className = 'selected-client-enhanced';
            selectedDisplay.innerHTML = `
                <div class="selected-client-icon">✓</div>
                <div class="selected-client-info">
                    <div class="selected-client-name">${nombre}</div>
                    <div class="selected-client-nit">NIT: ${nit}</div>
                </div>
                <button type="button" onclick="clearClientSelection()" class="btn-clear-selection">✕</button>
            `;
            selectedDisplay.style.display = 'flex';
        }

        // Mostrar toast
        ToastSystem.success(`Cliente "${nombre}" seleccionado correctamente`, '¡Cliente seleccionado!');
    };
}

// ========== 6. FAB BUTTONS (FLOATING ACTION BUTTONS) ==========
function initFABButtons() {
    // Crear contenedor FAB solo para el botón de Generar
    const fabContainer = document.createElement('div');
    fabContainer.className = 'fab-container';
    fabContainer.id = 'fab-container';

    // Solo botón Generar (FAB flotante)
    const fabGenerate = document.createElement('button');
    fabGenerate.type = 'button';
    fabGenerate.className = 'fab-button';
    fabGenerate.id = 'fab-generate';
    fabGenerate.style.display = 'none';
    fabGenerate.innerHTML = `
        <span class="fab-icon">📥</span>
        <span>Generar Cuenta de Cobro</span>
    `;
    fabGenerate.onclick = () => {
        if (ValidationSystem.validateForm()) {
            ConfirmationModal.show();
        }
    };

    fabContainer.appendChild(fabGenerate);
    document.body.appendChild(fabContainer);

    // NO ocultar el botón de vista previa original
    // Solo mejorar el botón de generar original
    const originalBtnGenerar = document.getElementById('btn-generar');
    if (originalBtnGenerar) {
        // Ocultar el botón original de generar cuando existe
        originalBtnGenerar.style.display = 'none';

        // Sincronizar visibilidad del FAB con el botón original
        const observer = new MutationObserver(() => {
            const originalGenerate = document.getElementById('btn-generar');
            if (originalGenerate && window.getComputedStyle(originalGenerate).display !== 'none') {
                fabGenerate.style.display = 'flex';
            } else {
                fabGenerate.style.display = 'none';
            }
        });

        observer.observe(originalBtnGenerar, { attributes: true, attributeFilter: ['style'] });
    }

    // Mejorar el botón de vista previa original con validación
    const originalBtnPreview = document.getElementById('btn-ver-preview');
    if (originalBtnPreview) {
        const originalOnClick = originalBtnPreview.onclick;
        originalBtnPreview.onclick = (e) => {
            if (ValidationSystem.validateForm()) {
                if (originalOnClick) {
                    originalOnClick.call(originalBtnPreview, e);
                } else {
                    showPreview();
                }
            }
        };
    }
}

// ========== 7. SUCCESS MODAL AFTER PDF GENERATION ==========
function showSuccessModal(pdfUrl, filename) {
    const modal = document.createElement('div');
    modal.className = 'confirm-modal';
    modal.style.display = 'block';

    // Construir URL completo para WhatsApp (necesitamos URL absoluto)
    const fullPdfUrl = window.location.origin + pdfUrl;

    // Mensaje predefinido para WhatsApp
    const whatsappMessage = encodeURIComponent(
        `¡Hola! 👋\n\nTe envío mi cuenta de cobro:\n📄 ${filename}\n\n` +
        `Puedes descargarla aquí:\n${fullPdfUrl}\n\n` +
        `¡Gracias!`
    );

    const whatsappUrl = `https://wa.me/?text=${whatsappMessage}`;

    modal.innerHTML = `
        <div class="confirm-modal-content">
            <div class="confirm-modal-header" style="background: linear-gradient(135deg, #10b981, #059669);">
                <div class="confirm-modal-icon">✅</div>
                <h2 class="confirm-modal-title">¡Cuenta de cobro generada!</h2>
            </div>
            <div class="confirm-modal-body">
                <p style="margin: 0 0 20px 0; color: var(--text-secondary); font-size: 14px; text-align: center;">
                    Tu cuenta de cobro ha sido generada exitosamente
                </p>
                <div style="background: var(--gray-50); border-radius: var(--radius-md); padding: 16px; text-align: center; margin-bottom: 20px;">
                    <p style="margin: 0; font-size: 13px; color: var(--text-secondary); margin-bottom: 8px;">Archivo generado:</p>
                    <p style="margin: 0; font-size: 14px; font-weight: 600; color: var(--text-primary); font-family: monospace;">${filename}</p>
                </div>
            </div>
            <div class="confirm-modal-footer" style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
                <button type="button" class="btn btn-secondary" style="grid-column: 1 / -1;" onclick="this.closest('.confirm-modal').remove(); location.href='/dashboard'">
                    Crear otra
                </button>
                <button type="button" class="btn btn-secondary" onclick="this.closest('.confirm-modal').remove(); document.getElementById('historial-section').scrollIntoView({behavior: 'smooth'})">
                    Ver en Historial
                </button>
                <button type="button" class="btn btn-primary" onclick="window.open('${pdfUrl}', '_blank')">
                    📥 Descargar
                </button>
                <button type="button" class="btn btn-success" style="grid-column: 1 / -1; background: linear-gradient(135deg, #25D366, #128C7E); border: none;" onclick="window.open('${whatsappUrl}', '_blank')">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" style="display: inline-block; margin-right: 8px; vertical-align: middle;">
                        <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z" fill="currentColor"/>
                    </svg>
                    Compartir por WhatsApp
                </button>
            </div>
        </div>
    `;

    document.body.appendChild(modal);

    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.remove();
        }
    });
}

// ========== INITIALIZATION ==========
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Inicializando mejoras UX de CobraFlow...');

    // Inicializar sistemas
    ToastSystem.init();
    ValidationSystem.initLiveValidation();
    initCharacterCounters();
    enhanceClientSelection();
    initFABButtons();

    console.log('✅ Mejoras UX cargadas correctamente');
});

// Exportar para uso global
window.ToastSystem = ToastSystem;
window.ValidationSystem = ValidationSystem;
window.ConfirmationModal = ConfirmationModal;
window.showSuccessModal = showSuccessModal;
