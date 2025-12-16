import { Button } from '@/components/ui/button';
import { ArrowRight, FileText, Share2, CreditCard } from 'lucide-react';

const Hero = () => {
  const redirectToApp = () => {
    // Redirige al login del backend
    const backendUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
    window.location.href = `${backendUrl}/login`;
  };

  return (
    <section className="relative pt-28 lg:pt-36 pb-20 lg:pb-32 hero-gradient overflow-hidden">
      {/* Background decoration */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-primary/5 rounded-full blur-3xl" />
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-accent/30 rounded-full blur-3xl" />
      </div>

      <div className="container-section relative">
        <div className="grid lg:grid-cols-2 gap-12 lg:gap-16 items-center">
          {/* Left Column - Content */}
          <div className="text-center lg:text-left">
            <div className="inline-flex items-center gap-2 bg-accent/50 rounded-full px-4 py-1.5 mb-6 animate-fade-up">
              <span className="w-2 h-2 bg-primary rounded-full animate-pulse" />
              <span className="text-sm font-medium text-accent-foreground">
                Por DT Growth Partners
              </span>
            </div>

            <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold text-foreground leading-tight mb-6 animate-fade-up animate-delay-100">
              Genera cuentas de cobro{' '}
              <span className="gradient-text">en segundos.</span>
            </h1>

            <p className="text-lg md:text-xl text-muted-foreground mb-8 max-w-xl mx-auto lg:mx-0 animate-fade-up animate-delay-200">
              Sin Excel. Sin complicaciones. Descarga tu archivo PDF listo para enviar y cobrar.
            </p>

            <div className="flex flex-col sm:flex-row gap-4 justify-center lg:justify-start animate-fade-up animate-delay-300">
              <Button
                variant="hero"
                size="xl"
                onClick={redirectToApp}
                className="group"
              >
                Probar Gratis Ahora
                <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
              </Button>
              <Button
                variant="outline"
                size="xl"
                onClick={() => document.getElementById('como-funciona')?.scrollIntoView({ behavior: 'smooth' })}
              >
                Ver cómo funciona
              </Button>
            </div>

            {/* Trust badges */}
            <div className="flex items-center gap-6 mt-10 justify-center lg:justify-start text-muted-foreground animate-fade-up animate-delay-400">
              <div className="flex items-center gap-2">
                <div className="flex -space-x-2">
                  {[1, 2, 3, 4].map((i) => (
                    <div
                      key={i}
                      className="w-8 h-8 rounded-full bg-gradient-to-br from-primary/20 to-accent border-2 border-background"
                    />
                  ))}
                </div>
                <span className="text-sm">+500 usuarios activos</span>
              </div>
            </div>
          </div>

          {/* Right Column - Invoice Mockup */}
          <div className="relative animate-fade-up animate-delay-200">
            <div className="relative mx-auto max-w-md lg:max-w-none">
              {/* Main card */}
              <div className="bg-card rounded-2xl shadow-elevated p-6 border border-border animate-float">
                <div className="flex items-center justify-between mb-6">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-lg gradient-bg flex items-center justify-center">
                      <FileText className="w-5 h-5 text-primary-foreground" />
                    </div>
                    <div>
                      <p className="font-semibold text-foreground">Cuenta de Cobro</p>
                      <p className="text-sm text-muted-foreground">#001-2024</p>
                    </div>
                  </div>
                  <span className="px-3 py-1 bg-green-100 text-green-700 rounded-full text-sm font-medium">
                    Generada
                  </span>
                </div>

                <div className="space-y-4 mb-6">
                  <div className="flex justify-between items-center py-3 border-b border-border">
                    <span className="text-muted-foreground">Emitido por</span>
                    <span className="font-medium text-foreground">Juan Pérez</span>
                  </div>
                  <div className="flex justify-between items-center py-3 border-b border-border">
                    <span className="text-muted-foreground">Cliente</span>
                    <span className="font-medium text-foreground">María García</span>
                  </div>
                  <div className="flex justify-between items-center py-3 border-b border-border">
                    <span className="text-muted-foreground">Concepto</span>
                    <span className="font-medium text-foreground">Diseño web</span>
                  </div>
                  <div className="flex justify-between items-center py-3">
                    <span className="text-muted-foreground">Monto</span>
                    <span className="text-2xl font-bold gradient-text">$850.000</span>
                  </div>
                </div>

                <div className="flex gap-3">
                  <Button variant="outline" size="sm" className="flex-1">
                    <Share2 className="w-4 h-4 mr-2" />
                    Compartir
                  </Button>
                  <Button variant="default" size="sm" className="flex-1">
                    <CreditCard className="w-4 h-4 mr-2" />
                    Cobrar
                  </Button>
                </div>
              </div>

              {/* Decorative elements */}
              <div className="absolute -top-4 -right-4 w-24 h-24 bg-primary/10 rounded-full blur-2xl" />
              <div className="absolute -bottom-4 -left-4 w-32 h-32 bg-accent/40 rounded-full blur-2xl" />
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Hero;
