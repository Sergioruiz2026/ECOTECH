import os
import smtplib
from email.message import EmailMessage


def enviar_codigo_verificacion(destinatario: str, codigo: str):
    host = os.getenv("ECOTECH_SMTP_HOST")
    usuario = os.getenv("ECOTECH_SMTP_USER")
    contraseña = os.getenv("ECOTECH_SMTP_PASSWORD")
    remitente = os.getenv("ECOTECH_SMTP_FROM", usuario)
    puerto = int(os.getenv("ECOTECH_SMTP_PORT", "587"))

    if not host or not usuario or not contraseña or not remitente:
        raise RuntimeError(
            "Falta configurar ECOTECH_SMTP_HOST, ECOTECH_SMTP_USER, "
            "ECOTECH_SMTP_PASSWORD y ECOTECH_SMTP_FROM."
        )

    mensaje = EmailMessage()
    mensaje["Subject"] = "Código de acceso ECOTECH"
    mensaje["From"] = remitente
    mensaje["To"] = destinatario
    mensaje.set_content(f"Su código de verificación ECOTECH es: {codigo}\nCaduca en 10 minutos.")

    try:
        with smtplib.SMTP(host, puerto, timeout=15) as servidor:
            servidor.starttls()
            servidor.login(usuario, contraseña)
            servidor.send_message(mensaje)
    except (OSError, smtplib.SMTPException) as error:
        raise RuntimeError(f"No se pudo enviar el correo de verificación: {error}") from error