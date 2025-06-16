import imaplib
import email
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import time
import re
import os

# Configuración del correo
EMAIL = "hoyquigadgets@gmail.com"
PASSWORD = "iqog tfjk lnpb nxxa"  # Contraseña de aplicación
IMAP_SERVER = "imap.gmail.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Número de WhatsApp
WHATSAPP_NUMBER = "+593961249195"
WHATSAPP_LINK = f"https://wa.me/{WHATSAPP_NUMBER}?text=¡Hola! 👋 Me interesa conocer más sobre sus productos tecnológicos. 🚀 Estoy buscando soluciones innovadoras para mis necesidades digitales. 💻 ¿Podrían brindarme información detallada sobre sus servicios y catálogo? 📱"

# Ruta de la imagen
IMAGE_PATH = "img/publicidad.jpg"

def connect_imap():
    """Conectar al servidor IMAP"""
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL, PASSWORD)
        return mail
    except Exception as e:
        print(f"❌ Error al conectar con IMAP: {str(e)}")
        return None

def send_response(to_email):
    """Enviar respuesta automática"""
    try:
        print(f"\n📤 Intentando enviar respuesta a: {to_email}")
        
        msg = MIMEMultipart()
        msg['From'] = EMAIL
        msg['To'] = to_email
        msg['Subject'] = "¡Gracias por contactar a TechGadgets! 🚀"

        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <h2>¡Gracias por contactarnos! 🎉</h2>
            <p>Hemos recibido tu mensaje y nos pondremos en contacto contigo pronto.</p>
            
            <div style="text-align: center; margin: 20px 0;">
                <img src="cid:publicidad" style="max-width: 100%; height: auto; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
            </div>
            
            <h3>📱 Contáctanos por WhatsApp</h3>
            <p>Para una respuesta más rápida, puedes contactarnos directamente por WhatsApp:</p>
            <p><a href="{WHATSAPP_LINK}" style="background-color: #25D366; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Contactar por WhatsApp</a></p>
            
            <h3>💻 Nuestros Servicios</h3>
            <ul>
                <li>Venta de productos tecnológicos</li>
                <li>Soporte post-venta</li>
                <li>Garantía en todos nuestros productos</li>
            </ul>
            
            <p>Saludos cordiales,<br>Equipo TechGadgets</p>
        </body>
        </html>
        """
        
        msg.attach(MIMEText(html, 'html'))
        
        # Adjuntar imagen si existe
        if os.path.exists(IMAGE_PATH):
            print("📷 Adjuntando imagen...")
            with open(IMAGE_PATH, 'rb') as f:
                img = MIMEImage(f.read())
                img.add_header('Content-ID', '<publicidad>')
                msg.attach(img)
            print("✅ Imagen adjuntada correctamente")
        else:
            print("⚠️ No se encontró la imagen en la ruta:", IMAGE_PATH)
        
        print("📧 Conectando al servidor SMTP...")
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            print("🔒 Iniciando conexión segura...")
            server.starttls()
            print("🔑 Iniciando sesión...")
            server.login(EMAIL, PASSWORD)
            print("📤 Enviando mensaje...")
            server.send_message(msg)
            
        print(f"✅ Respuesta enviada exitosamente a: {to_email}")
        return True
    except Exception as e:
        print(f"❌ Error al enviar respuesta: {str(e)}")
        print(f"Detalles del error: {type(e).__name__}")
        return False

def extract_email_from_formspree(body):
    """Extraer el correo del remitente del mensaje de Formspree"""
    # Intentar diferentes patrones comunes de Formspree
    patterns = [
        r'Email:\s*([^\n]+)',
        r'email:\s*([^\n]+)',
        r'From:\s*([^\n]+)',
        r'from:\s*([^\n]+)',
        r'Reply-To:\s*([^\n]+)',
        r'reply-to:\s*([^\n]+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, body, re.IGNORECASE)
        if match:
            email = match.group(1).strip()
            # Verificar que sea un correo válido
            if '@' in email and '.' in email:
                return email
    
    return None

def process_email(mail, num):
    """Procesar un correo individual"""
    try:
        _, msg = mail.fetch(num, '(RFC822)')
        email_body = msg[0][1]
        email_message = email.message_from_bytes(email_body)
        
        # Obtener información del correo
        from_email = email.utils.parseaddr(email_message['From'])[1]
        subject = email_message['Subject']
        
        print(f"\n📧 Procesando correo:")
        print(f"De: {from_email}")
        print(f"Asunto: {subject}")
        
        # Obtener el cuerpo del correo
        body = ""
        if email_message.is_multipart():
            for part in email_message.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode()
                    break
        else:
            body = email_message.get_payload(decode=True).decode()
        
        print(f"📝 Contenido del correo:")
        print(body)
        
        # Extraer el correo del remitente
        sender_email = extract_email_from_formspree(body)
        
        if sender_email:
            print(f"📧 Correo del remitente encontrado: {sender_email}")
            
            # Enviar respuesta automática
            if send_response(sender_email):
                # Marcar como leído y mover a la papelera
                mail.store(num, '+FLAGS', '\\Seen')
                mail.store(num, '+X-GM-LABELS', '\\Trash')
                print(f"✅ Correo procesado y movido a la papelera")
                return True
        else:
            print("❌ No se pudo encontrar el correo del remitente en el mensaje")
            print("Contenido del mensaje:")
            print(body)
        
        return False
    except Exception as e:
        print(f"❌ Error al procesar correo: {str(e)}")
        return False

def check_new_emails():
    """Verificar nuevos correos y enviar respuestas"""
    mail = connect_imap()
    if not mail:
        return
    
    try:
        mail.select('inbox')
        _, messages = mail.search(None, 'UNSEEN')
        
        if not messages[0]:
            print("📭 No hay correos nuevos")
            return
        
        print(f"📬 Encontrados {len(messages[0].split())} correos nuevos")
        
        for num in messages[0].split():
            process_email(mail, num)
            
    except Exception as e:
        print(f"❌ Error al verificar correos: {str(e)}")
    finally:
        try:
            mail.close()
            mail.logout()
        except:
            pass

def main():
    print("🚀 Iniciando sistema de respuesta automática de correos...")
    print("📧 Verificando nuevos correos cada 20 segundos...")
    
    while True:
        try:
            check_new_emails()
            print(f"\n⏳ Esperando 20 segundos para la siguiente verificación...")
            time.sleep(20)  # Esperar 20 segundos
        except Exception as e:
            print(f"❌ Error en el ciclo principal: {str(e)}")
            time.sleep(5)  # Esperar 5 segundos antes de reintentar

if __name__ == "__main__":
    main() 