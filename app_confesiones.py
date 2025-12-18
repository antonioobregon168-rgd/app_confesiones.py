import streamlit as st
import smtplib
from email.message import EmailMessage

# ===============================
# CONFIGURACIÓN DE LA PÁGINA
# ===============================
st.set_page_config(
    page_title="Confesiones Anónimas",
    page_icon="📩",
    layout="centered"
)

st.title("📩 Buzón de Confesiones")
st.write(
    "Envía una confesión de forma **anónima**. "
    "Si deseas respuesta, puedes dejar tu correo (opcional)."
)

st.divider()

# ===============================
# FORMULARIO
# ===============================
with st.form("form_confesion"):
    correo_usuario = st.text_input(
        "📧 Tu correo (opcional, solo si quieres respuesta)"
    )

    mensaje = st.text_area(
        "💬 Escribe tu confesión",
        placeholder="Aquí puedes escribir lo que quieras decir...",
        height=180
    )

    enviar = st.form_submit_button("📨 Enviar confesión")

# ===============================
# ENVÍO DE CORREO
# ===============================
if enviar:
    if mensaje.strip() == "":
        st.warning("⚠️ El mensaje no puede estar vacío")
    else:
        try:
            # 🔐 Datos desde st.secrets
            EMAIL_REMITENTE = st.secrets["EMAIL_REMITENTE"]
            CONTRASENA_APP = st.secrets["CONTRASENA_APP"]
            EMAIL_DESTINO = st.secrets["EMAIL_DESTINO"]

            # Crear email
            email = EmailMessage()
            email["From"] = EMAIL_REMITENTE
            email["To"] = EMAIL_DESTINO
            email["Subject"] = "📩 Nueva confesión recibida"

            # Si el usuario puso correo → Reply-To
            if correo_usuario:
                email["Reply-To"] = correo_usuario

            email.set_content(
                f"""
📩 NUEVA CONFESIÓN

Mensaje:
{mensaje}

Correo del remitente:
{correo_usuario if correo_usuario else "Anónimo"}
"""
            )

            # Enviar con Gmail
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(EMAIL_REMITENTE, CONTRASENA_APP)
                smtp.send_message(email)

            st.success("✅ Tu confesión fue enviada correctamente")
            st.balloons()

        except Exception as e:
            st.error("❌ Ocurrió un error al enviar el mensaje")
            st.code(str(e))

