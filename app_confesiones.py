import streamlit as st
import smtplib
from email.message import EmailMessage

# ===============================
# MODO MANTENIMIENTO
# ===============================
MODO_MANTENIMIENTO = True  # ⬅️ CAMBIA A True PARA CERRAR LA APP

if MODO_MANTENIMIENTO:
    st.set_page_config(
        page_title="En mantenimiento",
        page_icon="🛠️",
        layout="centered"
    )

    st.markdown(
        """
        <div style="
            background-color: white;
            padding: 50px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        ">
            <h1 style="color:black;">🚫 Página cerrada por el momento</h1>
            <p style="font-size:18px; color:black;">
                Lo sentimos, no se están recibiendo confesiones ahora.
            </p>
            <p style="margin-top:30px; color:gray;">
                Creada por <b>Antonio</b>
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.stop()

# ===============================
# CONFIGURACIÓN NORMAL
# ===============================
st.set_page_config(
    page_title="Confesiones",
    page_icon="📩",
    layout="centered"
)

st.title("📩 Buzón de Confesiones")
st.write(
    "Puedes enviar una confesión. "
    "Tu nombre y correo son opcionales si deseas respuesta."
)

st.divider()

# ===============================
# FORMULARIO
# ===============================
with st.form("form_confesion"):
    nombre = st.text_input("👤 Tu nombre (opcional)")
    correo = st.text_input("📧 Tu correo (opcional, para responderte)")
    confesion = st.text_area(
        "💬 Escribe tu confesión",
        placeholder="Escribe aquí lo que quieras confesar…",
        height=180
    )

    enviar = st.form_submit_button("📨 Enviar confesión")

# ===============================
# ENVÍO DE CORREO
# ===============================
if enviar:
    if confesion.strip() == "":
        st.warning("⚠️ La confesión no puede estar vacía")
    else:
        try:
            EMAIL_REMITENTE = st.secrets["EMAIL_REMITENTE"]
            CONTRASENA_APP = st.secrets["CONTRASENA_APP"]
            EMAIL_DESTINO = st.secrets["EMAIL_DESTINO"]

            email = EmailMessage()
            email["From"] = EMAIL_REMITENTE
            email["To"] = EMAIL_DESTINO
            email["Subject"] = "📩 Nueva confesión recibida"

            # Para que puedas responder directo
            if correo:
                email["Reply-To"] = correo

            email.set_content(
                f"""
📩 NUEVA CONFESIÓN RECIBIDA

👤 Nombre:
{nombre if nombre else "Anónimo"}

📧 Correo:
{correo if correo else "No proporcionado"}

💬 Confesión:
{confesion}
"""
            )

            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(EMAIL_REMITENTE, CONTRASENA_APP)
                smtp.send_message(email)

            st.success("✅ Confesión enviada correctamente")
            st.balloons()

        except Exception as e:
            st.error("❌ Error al enviar la confesión")
            st.code(str(e))


