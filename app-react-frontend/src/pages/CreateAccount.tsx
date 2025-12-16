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
    fecha: new Date().toLocaleDateString('es-CO').split('/').reverse().join('-'), // dd/mm/yyyy to yyyy-mm-dd? Wait, backend expects dd/mm/yyyy
  });

  const [servicios, setServicios] = useState<Servicio[]>([
    { descripcion: '', cantidad: 1, precio_unitario: 0 }
  ]);

  const [isLoading, setIsLoading] = useState(false);

  const handleInputChange = (field: string, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleServicioChange = (index: number, field: keyof Servicio, value: string | number) => {
    setServicios(prev => prev.map((serv, i) =>
      i === index ? { ...serv, [field]: value } : serv
    ));
  };

  const addServicio = () => {
    setServicios(prev => [...prev, { descripcion: '', cantidad: 1, precio_unitario: 0 }]);
  };

  const removeServicio = (index: number) => {
    if (servicios.length > 1) {
      setServicios(prev => prev.filter((_, i) => i !== index));
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!formData.nickname_cliente || !formData.concepto || servicios.some(s => !s.descripcion || s.precio_unitario <= 0)) {
      toast.error('Por favor completa todos los campos requeridos');
      return;
    }

    setIsLoading(true);

    try {
      const payload = {
        nickname_cliente: formData.nickname_cliente,
        valor: servicios.reduce((sum, s) => sum + (s.cantidad * s.precio_unitario), 0), // calculate total
        servicios,
        concepto: formData.concepto,
        fecha: new Date().toLocaleDateString('es-CO', { day: '2-digit', month: '2-digit', year: 'numeric' }).replace(/\//g, '/'), // formato dd/mm/yyyy
        servicio_proyecto: formData.servicio_proyecto,
      };

      const response = await fetch(`${API_URL}/crear-cuenta-simple/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      if (response.ok) {
        // The response is a PDF file
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

        // Resetear el formulario
        setFormData({
          nickname_cliente: '',
          concepto: '',
          servicio_proyecto: '',
          fecha: new Date().toLocaleDateString('es-CO').split('/').reverse().join('-'),
        });
        setServicios([{ descripcion: '', cantidad: 1, precio_unitario: 0 }]);
      } else {
        const error = await response.json();
        toast.error(error.detail || 'Error al generar la cuenta de cobro');
      }
    } catch (error) {
      console.error('Error:', error);
      toast.error('Error de conexión. Inténtalo de nuevo.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-background py-20">
      <div className="container-section max-w-2xl mx-auto">
        <div className="text-center mb-8">
          <h1 className="text-3xl md:text-4xl font-bold text-foreground mb-4">
            Crear Cuenta de Cobro
          </h1>
          <p className="text-lg text-muted-foreground">
            Genera tu cuenta de cobro profesional en segundos
          </p>
        </div>

        <div className="bg-card rounded-2xl shadow-elevated border border-border p-8">
          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="space-y-2">
              <Label htmlFor="nickname_cliente" className="text-foreground font-medium">
                Nombre del Cliente *
              </Label>
              <Input
                id="nickname_cliente"
                placeholder="Ej: María García o Empresa ABC"
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
                placeholder="Ej: Facturación de servicios de desarrollo web"
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
                    <span className="text-sm font-medium text-foreground">Servicio {index + 1}</span>
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

                  <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                    <div className="md:col-span-2">
                      <Input
                        placeholder="Descripción del servicio"
                        value={servicio.descripcion}
                        onChange={(e) => handleServicioChange(index, 'descripcion', e.target.value)}
                        required
                      />
                    </div>
                    <Input
                      type="number"
                      placeholder="Cantidad"
                      value={servicio.cantidad}
                      onChange={(e) => handleServicioChange(index, 'cantidad', parseInt(e.target.value) || 1)}
                      min="1"
                      required
                    />
                    <Input
                      type="number"
                      placeholder="Precio unitario"
                      value={servicio.precio_unitario}
                      onChange={(e) => handleServicioChange(index, 'precio_unitario', parseFloat(e.target.value) || 0)}
                      min="0"
                      step="0.01"
                      className="md:col-span-2"
                      required
                    />
                  </div>
                </div>
              ))}
            </div>

            <Button
              type="submit"
              variant="hero"
              size="xl"
              className="w-full"
              disabled={isLoading}
            >
              {isLoading ? (
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
  );
};

export default CreateAccount;