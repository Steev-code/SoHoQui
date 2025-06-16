# Sistema de Respuesta Automática de Correos 📧

## 📝 Descripción

Este sistema automatiza la gestión de correos electrónicos entrantes, enviando respuestas automáticas personalizadas a los remitentes. Está diseñado específicamente para trabajar con Formspree y Gmail, proporcionando una solución eficiente para la atención al cliente.

## ✨ Características

- 📬 Monitoreo automático de correos nuevos
- 📤 Respuestas automáticas personalizadas
- 🖼️ Soporte para imágenes en las respuestas
- 💬 Integración con WhatsApp
- 🔄 Procesamiento continuo cada 20 segundos
- 📝 Extracción inteligente de correos de Formspree
- 🗑️ Gestión automática de correos procesados

## 🚀 Tecnologías Utilizadas

- Python 3.x
- IMAP4 (Gmail)
- SMTP
- HTML para plantillas de correo
- Expresiones regulares

## 🛠️ Instalación

1. Clona el repositorio:
```bash
git clone https://github.com/tu-usuario/auto-email-responder.git
cd auto-email-responder
```

2. Crea un entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instala las dependencias:
```bash
pip install -r requirements.txt
```

4. Configura las variables de entorno:
```bash
# Crea un archivo .env con las siguientes variables:
EMAIL=tu_correo@gmail.com
PASSWORD=tu_contraseña_de_aplicacion
WHATSAPP_NUMBER=tu_numero_whatsapp
```

## ⚙️ Configuración

1. Configura una contraseña de aplicación en Gmail:
   - Ve a la configuración de tu cuenta de Google
   - Seguridad > Contraseñas de aplicación
   - Genera una nueva contraseña para la aplicación

2. Coloca tu imagen de publicidad:
   - Guarda tu imagen como `img/publicidad.jpg`

## 🚀 Uso

1. Ejecuta el script:
```bash
python email_responder.py
```

2. El sistema comenzará a monitorear automáticamente los correos entrantes.

## 📋 Estructura del Proyecto

```
auto-email-responder/
├── email_responder.py
├── requirements.txt
├── .env
├── img/
│   └── publicidad.jpg
└── README.md
```

## ⚠️ Consideraciones de Seguridad

- Nunca compartas tu archivo `.env`
- Mantén segura tu contraseña de aplicación
- No subas credenciales al repositorio

## 🔄 Mantenimiento

El script está diseñado para ejecutarse continuamente. Para mantenerlo en ejecución:

1. En Linux/Mac:
```bash
nohup python email_responder.py &
```

2. En Windows:
```bash
pythonw email_responder.py
```

## 📝 Logs

El sistema genera logs detallados de su funcionamiento, incluyendo:
- Conexiones exitosas/fallidas
- Correos procesados
- Errores encontrados
- Estado de las respuestas enviadas

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor, lee `CONTRIBUTING.md` para detalles sobre nuestro código de conducta y el proceso para enviarnos pull requests.

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles. 
