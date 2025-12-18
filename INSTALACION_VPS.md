# Guía de Instalación en VPS para CobraFlow

Este documento proporciona instrucciones paso a paso para instalar y configurar CobraFlow en tu VPS con el dominio `cobraflow.co`.

## Requisitos Previos

- Un VPS con Ubuntu 20.04 LTS o superior
- Acceso SSH al servidor
- Dominio `cobraflow.co` ya apuntando a la IP del VPS
- Conocimientos básicos de línea de comandos

## Paso 1: Conectarse al VPS

```bash
ssh usuario@cobraflow.co
```

Reemplaza `usuario` con tu nombre de usuario en el servidor.

## Paso 2: Actualizar el Sistema

```bash
sudo apt update && sudo apt upgrade -y
```

## Paso 3: Instalar Dependencias Necesarias

```bash
sudo apt install -y python3 python3-pip python3-venv git nginx certbot python3-dev libpq-dev postgresql postgresql-contrib
```

## Paso 4: Clonar el Repositorio

```bash
cd /opt
sudo git clone https://github.com/DTGrowthPartners/cobraflow.git
cd cobraflow
```

## Paso 5: Configurar Entorno Virtual

```bash
cd app-fastapi-backend
python3 -m venv venv
source venv/bin/activate
```

## Paso 6: Instalar Dependencias de Python

```bash
pip install -r requirements.txt
```

## Paso 7: Configurar Variables de Entorno

```bash
cp .env.example .env
nano .env
```

Edita el archivo `.env` con tus configuraciones:
- `SECRET_KEY`: Una clave secreta segura
- `DATABASE_URL`: Configuración de tu base de datos
- `GOOGLE_SHEETS_CREDENTIALS`: Ruta a tus credenciales de Google Sheets

## Paso 8: Configurar Nginx

```bash
sudo nano /etc/nginx/sites-available/cobraflow.co
```

Agrega la siguiente configuración:

```nginx
server {
    listen 80;
    server_name cobraflow.co www.cobraflow.co;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
    
    location /static/ {
        alias /opt/cobraflow/app-fastapi-backend/webapp/static/;
    }
    
    location /bases/ {
        alias /opt/cobraflow/app-fastapi-backend/;
    }
}
```

Habilita el sitio:

```bash
sudo ln -s /etc/nginx/sites-available/cobraflow.co /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## Paso 9: Configurar SSL con Certbot

```bash
sudo certbot --nginx -d cobraflow.co -d www.cobraflow.co
```

Sigue las instrucciones para obtener y configurar el certificado SSL. Certbot detectará automáticamente tu configuración de Nginx y configurará los certificados HTTPS para ambos dominios (con y sin www).

## Paso 10: Configurar el Servidor FastAPI

Crea un servicio systemd:

```bash
sudo nano /etc/systemd/system/cobraflow.service
```

Agrega el siguiente contenido:

```ini
[Unit]
Description=CobraFlow FastAPI Application
After=network.target

[Service]
User=usuario
Group=usuario
WorkingDirectory=/opt/cobraflow/app-fastapi-backend
Environment="PATH=/opt/cobraflow/app-fastapi-backend/venv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
ExecStart=/opt/cobraflow/app-fastapi-backend/venv/bin/uvicorn main:app --host 127.0.0.1 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

Reemplaza `usuario` con tu nombre de usuario.

Habilita y inicia el servicio:

```bash
sudo systemctl daemon-reload
sudo systemctl start cobraflow
sudo systemctl enable cobraflow
```

## Verificación del servicio

Para verificar que el servicio está funcionando correctamente:

```bash
sudo systemctl status cobraflow
```

## Comando alternativo para desarrollo

Si necesitas ejecutar el servidor manualmente para pruebas:

```bash
cd /opt/cobraflow/app-fastapi-backend
source venv/bin/activate
uvicorn main:app --host 127.0.0.1 --port 8000
```

## Paso 11: Configurar Firewall

```bash
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

## Paso 12: Verificar la Instalación

```bash
sudo systemctl status cobraflow
```

Abre tu navegador y visita:
- `https://cobraflow.co`
- `https://www.cobraflow.co`

Ambos dominios deben funcionar correctamente con HTTPS.

## Paso 13: Configuración Adicional (Opcional)

### Configurar Base de Datos PostgreSQL

```bash
sudo -u postgres psql
```

Dentro de PostgreSQL:

```sql
CREATE DATABASE cobraflow;
CREATE USER cobraflow_user WITH PASSWORD 'tu_contraseña_segura';
GRANT ALL PRIVILEGES ON DATABASE cobraflow TO cobraflow_user;
\q
```

Actualiza el archivo `.env` con la conexión a PostgreSQL:

```
DATABASE_URL=postgresql://cobraflow_user:tu_contraseña_segura@localhost/cobraflow
```

Reinicia el servicio:

```bash
sudo systemctl restart cobraflow
```

### Configurar Backups Automáticos

Crea un script de backup:

```bash
sudo nano /opt/cobraflow/backup.sh
```

Agrega:

```bash
#!/bin/bash
DATE=$(date +%Y-%m-%d)
BACKUP_DIR=/opt/cobraflow/backups
mkdir -p $BACKUP_DIR

# Backup de la base de datos
sudo -u postgres pg_dump -Fc cobraflow > $BACKUP_DIR/cobraflow_$DATE.dump

# Backup de los archivos generados
cp -r /opt/cobraflow/app-fastapi-backend/creadas $BACKUP_DIR/creadas_$DATE

# Comprimir backup
tar -czf $BACKUP_DIR/backup_$DATE.tar.gz $BACKUP_DIR/cobraflow_$DATE.dump $BACKUP_DIR/creadas_$DATE

# Eliminar backups antiguos (mantener 30 días)
find $BACKUP_DIR -name "backup_*.tar.gz" -mtime +30 -delete
```

Hazlo ejecutable:

```bash
chmod +x /opt/cobraflow/backup.sh
```

Configura un cron job:

```bash
sudo crontab -e
```

Agrega:

```
0 2 * * * /opt/cobraflow/backup.sh
```

Esto ejecutará el backup diariamente a las 2:00 AM.

## Solución de Problemas

### Problema: El servicio no inicia

Verifica los logs:

```bash
sudo journalctl -u cobraflow -f
```

### Problema: Errores de permisos

Asegúrate de que el usuario tenga permisos correctos:

```bash
sudo chown -R usuario:usuario /opt/cobraflow
```

### Problema: Nginx no encuentra archivos estáticos

Verifica las rutas en la configuración de Nginx y asegúrate de que los archivos existan:

```bash
ls -la /opt/cobraflow/app-fastapi-backend/webapp/static/
```

## Actualizaciones

Para actualizar la aplicación:

```bash
cd /opt/cobraflow
sudo git pull origin main
cd app-fastapi-backend
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart cobraflow
```

## Finalización

¡Felicidades! CobraFlow está instalado y configurado en tu VPS. Puedes acceder a la aplicación a través de `https://cobraflow.co`.

Si necesitas ayuda adicional, consulta el archivo `README.md` en el repositorio o contacta al equipo de soporte.