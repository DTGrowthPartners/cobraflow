import { Button } from '@/components/ui/button';
import { ArrowRight, Sparkles } from 'lucide-react';

const FinalCTA = () => {
  // URL del backend desde las variables de entorno
  const API_URL = import.meta.env.VITE_API_URL || '/api';

  const redirectToApp = () => {
    // Redirige al login de la aplicación FastAPI
    window.location.href = `${API_URL}/login`;
  };

  return (
    <section className="py-20 lg:py-32 bg-background relative overflow-hidden">
      {/* Background decoration */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-primary/5 rounded-full blur-3xl" />
      </div>

      <div className="container-section relative">
        <div className="max-w-3xl mx-auto text-center">
          <div className="inline-flex items-center gap-2 bg-accent rounded-full px-4 py-1.5 mb-6">
            <Sparkles className="w-4 h-4 text-primary" />
            <span className="text-sm font-medium text-accent-foreground">
              100% gratis para empezar
            </span>
          </div>

          <h2 className="text-3xl md:text-4xl lg:text-5xl font-bold text-foreground mb-6">
            Empieza a cobrar{' '}
            <span className="gradient-text">con estilo.</span>
          </h2>
          
          <p className="text-lg md:text-xl text-muted-foreground mb-10 max-w-xl mx-auto">
            CobraFlow es gratis para tus primeras cuentas. Sin tarjeta de crédito. Sin compromisos.
          </p>

          <Button
            variant="hero"
            size="xl"
            onClick={redirectToApp}
            className="group"
          >
            Probar Gratis Ahora
            <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
          </Button>

          <p className="mt-6 text-sm text-muted-foreground">
            Más de 500 freelancers y negocios ya usan CobraFlow
          </p>
        </div>
      </div>
    </section>
  );
};

export default FinalCTA;
