const Footer = () => {
  return (
    <footer className="py-12 bg-foreground text-background">
      <div className="container-section">
        <div className="flex flex-col md:flex-row items-center justify-between gap-6">
          {/* Logo */}
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-background/10 flex items-center justify-center">
              <span className="font-bold text-lg">C</span>
            </div>
            <span className="font-bold text-xl">CobraFlow</span>
          </div>

          {/* Links */}
          <nav className="flex items-center gap-6 text-sm text-background/70">
            <a href="#como-funciona" className="hover:text-background transition-colors">
              Cómo funciona
            </a>
            <a href="#beneficios" className="hover:text-background transition-colors">
              Beneficios
            </a>
            <a href="#generador" className="hover:text-background transition-colors">
              Probar Gratis
            </a>
          </nav>

          {/* Credits */}
          <p className="text-sm text-background/50">
            Hecho con ♥ por{' '}
            <span className="text-background/70 font-medium">DT Growth Partners</span>
          </p>
        </div>

        <div className="border-t border-background/10 mt-8 pt-8 text-center text-sm text-background/50">
          <p>© {new Date().getFullYear()} CobraFlow. Todos los derechos reservados.</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
