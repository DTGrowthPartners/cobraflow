import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { useNavigate } from 'react-router-dom';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { toast } from 'sonner';
import { FileText, Copy, Share2, Check, Sparkles, Lock } from 'lucide-react';

const STORAGE_KEY = 'cobraflow_usage_count';
const MAX_FREE_USES = 3;

interface GeneratedInvoice {
  clientName: string;
  amount: string;
  description: string;
  paymentMethod: string;
  id: string;
  date: string;
}

const InvoiceGenerator = () => {
  const navigate = useNavigate();

  const [usageCount, setUsageCount] = useState(0);
  const [showCaptureModal, setShowCaptureModal] = useState(false);
  const [showInvoiceModal, setShowInvoiceModal] = useState(false);
  const [generatedInvoice, setGeneratedInvoice] = useState<GeneratedInvoice | null>(null);
  const [copied, setCopied] = useState(false);
  const [contactInfo, setContactInfo] = useState('');

  const [formData, setFormData] = useState({
    clientName: '',
    amount: '',
    description: '',
    paymentMethod: '',
  });

  useEffect(() => {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored) {
      setUsageCount(parseInt(stored, 10));
    }
  }, []);

  const handleInputChange = (field: string, value: string) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
  };

  const formatCurrency = (value: string) => {
    const numbers = value.replace(/\D/g, '');
    return numbers ? `$${parseInt(numbers).toLocaleString('es-CO')}` : '';
  };

  const generateInvoice = () => {
    navigate('/crear-cuenta');
  };

  const handleContactSubmit = () => {
    if (!contactInfo) {
      toast.error('Por favor ingresa tu correo o número de teléfono');
      return;
    }
    
    // Here you would typically send this to your backend
    console.log('Contact info submitted:', contactInfo);
    toast.success('¡Gracias! Te contactaremos pronto para continuar usando CobraFlow.');
    setShowCaptureModal(false);
    setContactInfo('');
  };

  const copyLink = () => {
    const fakeLink = `https://cobraflow.app/c/${generatedInvoice?.id}`;
    navigator.clipboard.writeText(fakeLink);
    setCopied(true);
    toast.success('Link copiado al portapapeles');
    setTimeout(() => setCopied(false), 2000);
  };

  const shareWhatsApp = () => {
    const message = encodeURIComponent(
      `Hola, te comparto mi cuenta de cobro:\n\n` +
      `📝 ${generatedInvoice?.description}\n` +
      `💰 ${generatedInvoice?.amount}\n\n` +
      `Ver detalles: https://cobraflow.app/c/${generatedInvoice?.id}`
    );
    window.open(`https://wa.me/?text=${message}`, '_blank');
  };

  const remainingUses = MAX_FREE_USES - usageCount;
  const paymentMethods = [
    { value: 'efectivo', label: 'Efectivo' },
    { value: 'transferencia', label: 'Transferencia bancaria' },
    { value: 'link', label: 'Link de pago' },
  ];

  return (
    <section id="generador" className="py-20 lg:py-32 bg-secondary/30">
      <div className="container-section">
        <div className="text-center mb-12">
          <div className="inline-flex items-center gap-2 bg-accent rounded-full px-4 py-1.5 mb-4">
            <Sparkles className="w-4 h-4 text-primary" />
            <span className="text-sm font-medium text-accent-foreground">
              {remainingUses > 0
                ? `${remainingUses} uso${remainingUses > 1 ? 's' : ''} gratis restante${remainingUses > 1 ? 's' : ''}`
                : 'Límite gratuito alcanzado'}
            </span>
          </div>
          <h2 className="text-3xl md:text-4xl lg:text-5xl font-bold text-foreground mb-4">
            Genera tu cuenta de cobro
          </h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Completa los datos y obtén un link profesional para compartir con tu cliente
          </p>
        </div>

        <div className="max-w-2xl mx-auto">
          <div className="bg-card rounded-2xl shadow-elevated border border-border p-8">
            <div className="space-y-6">
              <div className="space-y-2">
                <Label htmlFor="clientName" className="text-foreground font-medium">
                  Nombre del cliente
                </Label>
                <Input
                  id="clientName"
                  placeholder="Ej: María García"
                  value={formData.clientName}
                  onChange={(e) => handleInputChange('clientName', e.target.value)}
                  className="h-12"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="amount" className="text-foreground font-medium">
                  Monto a cobrar
                </Label>
                <Input
                  id="amount"
                  placeholder="$0"
                  value={formData.amount}
                  onChange={(e) => handleInputChange('amount', formatCurrency(e.target.value))}
                  className="h-12 text-lg font-semibold"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="description" className="text-foreground font-medium">
                  Descripción del cobro
                </Label>
                <Textarea
                  id="description"
                  placeholder="Ej: Diseño de logo y manual de marca"
                  value={formData.description}
                  onChange={(e) => handleInputChange('description', e.target.value)}
                  className="min-h-[100px] resize-none"
                />
              </div>

              <div className="space-y-2">
                <Label className="text-foreground font-medium">Método de pago</Label>
                <Select
                  value={formData.paymentMethod}
                  onValueChange={(value) => handleInputChange('paymentMethod', value)}
                >
                  <SelectTrigger className="h-12">
                    <SelectValue placeholder="Selecciona un método" />
                  </SelectTrigger>
                  <SelectContent>
                    {paymentMethods.map((method) => (
                      <SelectItem key={method.value} value={method.value}>
                        {method.label}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <Button
                variant="hero"
                size="xl"
                className="w-full"
                onClick={generateInvoice}
                disabled={remainingUses <= 0}
              >
                {remainingUses > 0 ? (
                  <>
                    <FileText className="w-5 h-5" />
                    Generar cuenta de cobro
                  </>
                ) : (
                  <>
                    <Lock className="w-5 h-5" />
                    Desbloquear más cuentas
                  </>
                )}
              </Button>
            </div>
          </div>
        </div>

        {/* Generated Invoice Modal */}
        <Dialog open={showInvoiceModal} onOpenChange={setShowInvoiceModal}>
          <DialogContent className="sm:max-w-md">
            <DialogHeader>
              <DialogTitle className="flex items-center gap-2">
                <div className="w-8 h-8 rounded-lg gradient-bg flex items-center justify-center">
                  <FileText className="w-4 h-4 text-primary-foreground" />
                </div>
                Cuenta de Cobro Generada
              </DialogTitle>
              <DialogDescription>
                Tu cuenta de cobro está lista para compartir
              </DialogDescription>
            </DialogHeader>

            {generatedInvoice && (
              <div className="space-y-4">
                <div className="bg-secondary/50 rounded-xl p-4 space-y-3">
                  <div className="flex justify-between text-sm">
                    <span className="text-muted-foreground">ID</span>
                    <span className="font-mono font-medium text-foreground">{generatedInvoice.id}</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-muted-foreground">Cliente</span>
                    <span className="font-medium text-foreground">{generatedInvoice.clientName}</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-muted-foreground">Concepto</span>
                    <span className="font-medium text-foreground">{generatedInvoice.description}</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-muted-foreground">Método</span>
                    <span className="font-medium text-foreground capitalize">{generatedInvoice.paymentMethod}</span>
                  </div>
                  <div className="border-t border-border pt-3 flex justify-between">
                    <span className="text-muted-foreground">Monto</span>
                    <span className="text-xl font-bold gradient-text">{generatedInvoice.amount}</span>
                  </div>
                </div>

                <div className="flex gap-3">
                  <Button variant="outline" className="flex-1" onClick={copyLink}>
                    {copied ? <Check className="w-4 h-4" /> : <Copy className="w-4 h-4" />}
                    {copied ? 'Copiado' : 'Copiar link'}
                  </Button>
                  <Button variant="default" className="flex-1 bg-green-600 hover:bg-green-700" onClick={shareWhatsApp}>
                    <Share2 className="w-4 h-4" />
                    WhatsApp
                  </Button>
                </div>
              </div>
            )}
          </DialogContent>
        </Dialog>

        {/* Contact Capture Modal */}
        <Dialog open={showCaptureModal} onOpenChange={setShowCaptureModal}>
          <DialogContent className="sm:max-w-md">
            <DialogHeader>
              <DialogTitle className="flex items-center gap-2">
                <Sparkles className="w-5 h-5 text-primary" />
                ¡Te quedan muchas cuentas por crear!
              </DialogTitle>
              <DialogDescription>
                Deja tu correo o WhatsApp para desbloquear cuentas ilimitadas
              </DialogDescription>
            </DialogHeader>

            <div className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="contact">Correo o número de WhatsApp</Label>
                <Input
                  id="contact"
                  placeholder="correo@ejemplo.com o +57 300 123 4567"
                  value={contactInfo}
                  onChange={(e) => setContactInfo(e.target.value)}
                  className="h-12"
                />
              </div>

              <Button variant="hero" className="w-full" onClick={handleContactSubmit}>
                Continuar usando CobraFlow
              </Button>

              <p className="text-xs text-muted-foreground text-center">
                No spam. Solo te contactaremos para ayudarte a cobrar más fácil.
              </p>
            </div>
          </DialogContent>
        </Dialog>
      </div>
    </section>
  );
};

export default InvoiceGenerator;
