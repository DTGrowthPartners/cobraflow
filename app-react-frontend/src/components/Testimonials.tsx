import { Star } from 'lucide-react';

const testimonials = [
  {
    name: 'Ana Rodríguez',
    role: 'Diseñadora Freelancer',
    content: 'Antes lo hacía todo en Excel. Ahora genero mis cobros en segundos desde el celular. Mis clientes hasta me felicitan por lo profesional.',
    avatar: 'A',
  },
  {
    name: 'Carlos Méndez',
    role: 'Dueño de tienda',
    content: 'Tengo una tienda pequeña y esto me cambió la vida. Ya no tengo que hacer cuentas a mano ni perder facturas. Todo queda organizado.',
    avatar: 'C',
  },
  {
    name: 'Laura Gómez',
    role: 'Community Manager',
    content: 'Lo comparto directo por WhatsApp y mis clientes pagan más rápido. Es como magia. Ojalá lo hubiera encontrado antes.',
    avatar: 'L',
  },
];

const Testimonials = () => {
  return (
    <section className="py-20 lg:py-32 bg-secondary/30">
      <div className="container-section">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl lg:text-5xl font-bold text-foreground mb-4">
            Lo que dicen nuestros usuarios
          </h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Freelancers y negocios que ya cobran más fácil
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-6 lg:gap-8">
          {testimonials.map((testimonial, index) => (
            <div
              key={index}
              className="bg-card rounded-2xl p-6 lg:p-8 border border-border hover:shadow-soft transition-all duration-300"
            >
              {/* Stars */}
              <div className="flex gap-1 mb-4">
                {[...Array(5)].map((_, i) => (
                  <Star key={i} className="w-5 h-5 fill-primary text-primary" />
                ))}
              </div>
              
              {/* Quote */}
              <p className="text-foreground leading-relaxed mb-6">
                "{testimonial.content}"
              </p>
              
              {/* Author */}
              <div className="flex items-center gap-3">
                <div className="w-12 h-12 rounded-full gradient-bg flex items-center justify-center text-primary-foreground font-bold text-lg">
                  {testimonial.avatar}
                </div>
                <div>
                  <p className="font-semibold text-foreground">{testimonial.name}</p>
                  <p className="text-sm text-muted-foreground">{testimonial.role}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Testimonials;
