import { FileEdit, FileText, Share2, CheckCircle } from 'lucide-react';

const steps = [
  {
    icon: FileEdit,
    title: 'Rellena los datos',
    description: 'Tu nombre, cliente, monto, concepto y forma de pago.',
  },
  {
    icon: FileText,
    title: 'Descarga tu archivo',
    description: 'PDF profesional generado al instante, listo para enviar.',
  },
  {
    icon: Share2,
    title: 'Comparte por WhatsApp',
    description: 'Un clic y tu cliente recibe la cuenta de cobro.',
  },
  {
    icon: CheckCircle,
    title: 'Cobra sin complicaciones',
    description: 'Todo claro, todo profesional. Sin confusiones.',
  },
];

const HowItWorks = () => {
  return (
    <section id="como-funciona" className="py-20 lg:py-32 bg-background">
      <div className="container-section">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl lg:text-5xl font-bold text-foreground mb-4">
            Cobra en 4 pasos. Simple.
          </h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Genera tu primera cuenta de cobro en menos de 60 segundos
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
          {steps.map((step, index) => (
            <div
              key={index}
              className="relative group"
            >
              {/* Connector line */}
              {index < steps.length - 1 && (
                <div className="hidden lg:block absolute top-12 left-[60%] w-[80%] h-0.5 bg-gradient-to-r from-primary/30 to-transparent" />
              )}
              
              <div className="bg-card rounded-2xl p-6 border border-border hover:border-primary/30 transition-all duration-300 hover:shadow-soft group-hover:-translate-y-1">
                {/* Step number */}
                <div className="absolute -top-3 -left-3 w-8 h-8 rounded-full gradient-bg flex items-center justify-center text-primary-foreground font-bold text-sm shadow-soft">
                  {index + 1}
                </div>
                
                {/* Icon */}
                <div className="w-14 h-14 rounded-xl bg-accent flex items-center justify-center mb-5 group-hover:scale-110 transition-transform duration-300">
                  <step.icon className="w-7 h-7 text-primary" />
                </div>
                
                {/* Content */}
                <h3 className="text-lg font-semibold text-foreground mb-2">
                  {step.title}
                </h3>
                <p className="text-muted-foreground text-sm leading-relaxed">
                  {step.description}
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default HowItWorks;
