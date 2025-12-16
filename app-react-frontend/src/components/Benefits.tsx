import { Clock, Award, Target, Smartphone } from 'lucide-react';

const benefits = [
  {
    icon: Clock,
    title: 'Ahorra tiempo',
    description: 'Genera cuentas de cobro en segundos, no en minutos buscando plantillas.',
  },
  {
    icon: Award,
    title: 'Más profesional que Excel',
    description: 'Impresiona a tus clientes con cobros elegantes y fáciles de entender.',
  },
  {
    icon: Target,
    title: 'Cobra sin confusiones',
    description: 'Cada cobro tiene su propio link único. No más correos perdidos.',
  },
  {
    icon: Smartphone,
    title: 'Ideal para freelancers',
    description: 'Perfecto para freelancers, tiendas y negocios sin sistemas complicados.',
  },
];

const Benefits = () => {
  return (
    <section id="beneficios" className="py-20 lg:py-32 bg-background">
      <div className="container-section">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl lg:text-5xl font-bold text-foreground mb-4">
            ¿Por qué CobraFlow?
          </h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Diseñado para que cobrar sea tan fácil como enviar un mensaje
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-6 lg:gap-8 max-w-4xl mx-auto">
          {benefits.map((benefit, index) => (
            <div
              key={index}
              className="group relative bg-card rounded-2xl p-8 border border-border hover:border-primary/30 transition-all duration-300 hover:shadow-soft"
            >
              {/* Gradient background on hover */}
              <div className="absolute inset-0 rounded-2xl bg-gradient-to-br from-primary/5 to-accent/10 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
              
              <div className="relative">
                {/* Icon */}
                <div className="w-14 h-14 rounded-xl gradient-bg flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300 shadow-soft">
                  <benefit.icon className="w-7 h-7 text-primary-foreground" />
                </div>
                
                {/* Content */}
                <h3 className="text-xl font-semibold text-foreground mb-3">
                  {benefit.title}
                </h3>
                <p className="text-muted-foreground leading-relaxed">
                  {benefit.description}
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Benefits;
