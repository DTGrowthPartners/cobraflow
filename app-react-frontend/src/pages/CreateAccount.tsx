import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { toast } from 'sonner';
import { FileText, Plus, Trash2 } from 'lucide-react';

interface Servicio {
  descripcion: string;
  cantidad: number;
  precio_unitario: number;
}

const CreateAccount = () => {
  const API_URL = import.meta.env.VITE_API_URL || '/api';

  const [formData, setFormData] = useState({
    nickname_cliente: '',
    concepto: '',
    servicio_proyecto: '',
  });

  const [servicios, setServicios] = useState<Servicio[]>([
    { descripcion: '', cantidad: 1, precio_unitario: 0 }
  ]);

  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleInputChange = (field: string, value: string) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
  };

  const handleServicioChange = (index: number, field: string, value: string | number) => {
    setServicios((prev) =>
      prev.map((servicio, i) =>
        i === index ? { ...servicio, [field]: value } : servicio
      )
    );
  };

  const addServicio = () => {
    setServicios((prev) => [...prev, { descripcion: '', cantidad: 1, precio_unitario: 0 }]);
  };

  const removeServicio = (index: number) => {
    if (servicios.length > 1) {
      setServicios((prev) => prev.filter((_, i) => i !== index));
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!formData.nickname_cliente || !formData.concepto || servicios.some(s => !s.descripcion || s.cantidad <= 0 || s.precio_unitario <= 0)) {
      toast.error('Por favor completa todos los campos requeridos');
      return;
    }

    setIsSubmitting(true);

    try {
      const payload = {
        nickname_cliente: formData.nickname_cliente,
        valor: servicios.reduce((sum, s) => sum + (s.cantidad * s.precio_unitario), 0),
        servicios: servicios.map(s => ({
          descripcion: s.descripcion,
          cantidad: s.cantidad,
          precio_unitario: s.precio_unitario
        })),
        concepto: formData.concepto,
        servicio_proyecto: formData.servicio_proyecto,
      };

      const response = await fetch(`${API_URL}/crear-cuenta/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      if (response.ok) {
        // Download the PDF
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `cuenta_cobro_${formData.nickname_cliente}_${Date.now()}.pdf`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);

        toast.success('Cuenta de cobro generada exitosamente');
      } else {
        const error = await response.json();
        toast.error(error.detail || 'Error al generar la cuenta de cobro');
      }
    } catch (error) {
      console.error('Error:', error);
      toast.error('Error al conectar con el servidor');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen bg-background py-20 lg:py-32">
      <div className="container-section">
        <div className="max-w-2xl mx-auto">
          <div className="text-center mb-8">
            <h1 className="text-3xl md:text-4xl font-bold text-foreground mb-4">
              Crear Cuenta de Cobro
            </h1>
            <p className="text-muted-foreground">
              Completa los datos para generar tu cuenta de cobro profesional
            </p>
          </div>

          <div className="bg-card rounded-2xl shadow-elevated border border-border p-8">
            <form onSubmit={handleSubmit} className="space-y-6">
              <div className="space-y-2">
                <Label htmlFor="nickname_cliente" className="text-foreground font-medium">
                  Nickname del Cliente *
                </Label>
                <Input
                  id="nickname_cliente"
                  placeholder="Ej: maria_garcia"
                  value={formData.nickname_cliente}
                  onChange={(e) => handleInputChange('nickname_cliente', e.target.value)}
                  className="h-12"
                  required
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="concepto" className="text-foreground font-medium">
                  Concepto *
                </Label>
                <Textarea
                  id="concepto"
                  placeholder="Ej: Facturación de servicios de diseño web"
                  value={formData.concepto}
                  onChange={(e) => handleInputChange('concepto', e.target.value)}
                  className="min-h-[80px] resize-none"
                  required
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="servicio_proyecto" className="text-foreground font-medium">
                  Servicio/Proyecto
                </Label>
                <Input
                  id="servicio_proyecto"
                  placeholder="Ej: Desarrollo Web, Marketing Digital"
                  value={formData.servicio_proyecto}
                  onChange={(e) => handleInputChange('servicio_proyecto', e.target.value)}
                  className="h-12"
                />
              </div>

              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <Label className="text-foreground font-medium">Servicios *</Label>
                  <Button type="button" variant="outline" size="sm" onClick={addServicio}>
                    <Plus className="w-4 h-4 mr-2" />
                    Agregar Servicio
                  </Button>
                </div>

                {servicios.map((servicio, index) => (
                  <div key={index} className="bg-secondary/50 rounded-lg p-4 space-y-3">
                    <div className="flex items-center justify-between">
                      <span className="font-medium text-sm">Servicio {index + 1}</span>
                      {servicios.length > 1 && (
                        <Button
                          type="button"
                          variant="ghost"
                          size="sm"
                          onClick={() => removeServicio(index)}
                          className="text-destructive hover:text-destructive"
                        >
                          <Trash2 className="w-4 h-4" />
                        </Button>
                      )}
                    </div>

                    <div className="space-y-2">
                      <Label className="text-sm">Descripción *</Label>
                      <Textarea
                        placeholder="Ej: Diseño de logo"
                        value={servicio.descripcion}
                        onChange={(e) => handleServicioChange(index, 'descripcion', e.target.value)}
                        className="min-h-[60px] resize-none"
                        required
                      />
                    </div>

                    <div className="grid grid-cols-2 gap-3">
                      <div className="space-y-2">
                        <Label className="text-sm">Cantidad *</Label>
                        <Input
                          type="number"
                          min="1"
                          value={servicio.cantidad}
                          onChange={(e) => handleServicioChange(index, 'cantidad', parseInt(e.target.value) || 1)}
                          className="h-10"
                          required
                        />
                      </div>
                      <div className="space-y-2">
                        <Label className="text-sm">Precio Unitario *</Label>
                        <Input
                          type="number"
                          min="0"
                          step="0.01"
                          value={servicio.precio_unitario}
                          onChange={(e) => handleServicioChange(index, 'precio_unitario', parseFloat(e.target.value) || 0)}
                          className="h-10"
                          required
                        />
                      </div>
                    </div>

                    <div className="text-right text-sm text-muted-foreground">
                      Subtotal: ${(servicio.cantidad * servicio.precio_unitario).toLocaleString('es-CO')}
                    </div>
                  </div>
                ))}

                <div className="border-t border-border pt-4">
                  <div className="text-right text-lg font-semibold">
                    Total: ${servicios.reduce((sum, s) => sum + (s.cantidad * s.precio_unitario), 0).toLocaleString('es-CO')}
                  </div>
                </div>
              </div>

              <Button
                type="submit"
                variant="hero"
                size="xl"
                className="w-full"
                disabled={isSubmitting}
              >
                {isSubmitting ? (
                  'Generando...'
                ) : (
                  <>
                    <FileText className="w-5 h-5 mr-2" />
                    Generar Cuenta de Cobro
                  </>
                )}
              </Button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CreateAccount;