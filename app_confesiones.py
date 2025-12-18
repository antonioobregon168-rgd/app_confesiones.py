import streamlit as st
import smtplib
from email.message import EmailMessage

# ===============================
# CONFIGURACIÓN CORREO
# ===============================
CORREO_RECEPTOR = antonioobregon168@gmail.com      # AQUÍ VA TU CORREO
CORREO_EMISOR = antonioobregon168@gmail.com      # el mismo
CONTRASENA_APP = oqbg sipv eztv wuzv      # contraseña de aplicación

# ===============================
# MODO MANTENIMIENTO
# ===============================
MODO_MANTENIMIENTO = False

if MODO_MANTENIMIENTO:
    st.set_page_config(page_title="En mantenimiento", page_icon="🛠️")
    st.markdown("""
        <div style="
            background-color:white;
            color:black;
            padding:40px;
            margin-top:100px;
            border-radius:15px;
            text-align:center;
            box-shadow:0px 10px 30px rgba(0,0,0,0.15);
        ">
            <h1>🛠️ En mantenimiento</h1>
            <p>La app está siendo actualizada</p>
            <p><b>Por Antonio</b> 👨‍💻</p>
        </div>
    """, unsafe_allow_html=True)
    st.stop()

# ===============================
# CONFIGURACIÓN APP
# ===============================
st.set_page_config(
    page_title="Confesiones Anónimas",
    page_icon="📩",
    layout="centered"
)

st.title("📩 Buzón de Confesiones")
st.write("Envía un mensaje de forma anónima y segura.")

st.info("⚠️ Usa esta app con respeto. No envíes amenazas ni contenido ofensivo.")

# ===============================
# FORMULARIO
# ===============================
with st.form("form_confesion"):
    nombre = st.text_input("Tu nombre (opcional)")
    mensaje = st.text_area("Escribe tu confesión", max_chars=500)
    enviar = st.form_submit_button("📨 Enviar mensaje")

# ===============================
# ENVÍO DE CORREO
# ===============================
if enviar:
    if mensaje.strip() == "":
        st.error("❌ El mensaje no puede estar vacío")
    else:
        try:
            email = EmailMessage()
            email["From"] = CORREO_EMISOR
            email["To"] = CORREO_RECEPTOR
            email["Subject"] = "📩 Nueva confesión recibida"

            contenido = f"""
Nueva confesión recibida:

Nombre: {nombre if nombre else "Anónimo"}

Mensaje:
{mensaje}
"""
            email.set_content(contenido)

            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(CORREO_EMISOR, CONTRASENA_APP)
                smtp.send_message(email)

            st.success("✅ Mensaje enviado correctamente. Gracias por compartir.")

        except Exception as e:
            st.error("❌ Error al enviar el mensaje. Intenta más tarde.")

