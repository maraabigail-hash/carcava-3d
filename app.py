import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(
    page_title="Cárcava 3D",
    page_icon="🌱",
    layout="wide"
)

# Estilo visual
st.markdown("""
<style>
.stApp {
    background: #F5F7F1;
}
[data-testid="stSidebar"] {
    background: #E4EDE2;
}
h1, h2, h3 {
    color: #244C3A;
}
div.stButton > button {
    border-radius: 10px;
    min-height: 42px;
}
</style>
""", unsafe_allow_html=True)

# Navegación
st.sidebar.title("🌱 Cárcava 3D")
st.sidebar.caption("Análisis y recuperación del suelo")

paginas = [
    "Inicio",
    "Nueva cárcava",
    "Visor 3D",
    "Relleno y materiales",
    "Mis proyectos",
    "Informes"
]

if "pagina" not in st.session_state:
    st.session_state.pagina = "Inicio"

pagina = st.sidebar.radio(
    "MENÚ",
    paginas,
    key="navegacion",
    index=paginas.index(st.session_state.pagina)
)

st.session_state.pagina = pagina

# Datos de demostración
if "proyectos" not in st.session_state:
    st.session_state.proyectos = []

# INICIO
if pagina == "Inicio":
    st.title("Cárcava 3D")
    st.write(
        "Una plataforma para analizar la erosión "
        "y planificar la recuperación del terreno."
    )

    a, b, c = st.columns(3)
    a.metric("Proyectos", len(st.session_state.proyectos))
    b.metric("Modelos 3D", "0", "Pendiente de integrar")
    c.metric("IA", "Modo de prueba")

    st.subheader("¿Qué deseas hacer?")

    a, b = st.columns(2)
    with a:
        st.info("📷 **Crear un proyecto**")
        if st.button("Nueva cárcava", use_container_width=True):
            st.session_state.pagina = "Nueva cárcava"
            st.rerun()

    with b:
        st.info("🧊 **Explorar el terreno**")
        if st.button("Abrir visor 3D", use_container_width=True):
            st.session_state.pagina = "Visor 3D"
            st.rerun()

# NUEVA CÁRCAVA
elif pagina == "Nueva cárcava":
    st.title("Nueva cárcava")
    st.write("Registra un terreno para iniciar su análisis.")

    with st.form("nueva_carcava"):
        nombre = st.text_input("Nombre del proyecto")
        ubicacion = st.text_input("Ubicación")
        foto = st.file_uploader(
            "Fotografía del terreno",
            type=["jpg", "jpeg", "png"]
        )
        notas = st.text_area("Observaciones")

        guardar = st.form_submit_button(
            "Crear proyecto",
            type="primary"
        )

    if foto:
        st.image(foto, caption="Imagen original",
                 use_container_width=True)

    if guardar:
        if not nombre.strip():
            st.error("Escribe un nombre para el proyecto.")
        else:
            st.session_state.proyectos.append({
                "nombre": nombre.strip(),
                "ubicacion": ubicacion,
                "observaciones": notas,
                "archivo": foto.name if foto else None
            })
            st.success(
                "Proyecto creado en esta sesión. "
                "El almacenamiento permanente se integrará después."
            )

# VISOR 3D
elif pagina == "Visor 3D":
    st.title("Visor tridimensional")
    st.caption("Vista demostrativa, no representa una medición real.")

    x = np.linspace(-2, 2, 35)
    y = np.linspace(-2, 2, 35)
    X, Y = np.meshgrid(x, y)

    Z = 0.8 * np.exp(
        -(X**2 / 1.2 + Y**2 / 0.35)
    )

    fig = go.Figure(data=[
        go.Surface(x=X, y=Y, z=Z, colorscale="Earth")
    ])

    fig.update_layout(
        height=560,
        scene=dict(
            xaxis_title="X (m)",
            yaxis_title="Y (m)",
            zaxis_title="Z (m)"
        ),
        margin=dict(l=0, r=0, t=20, b=0)
    )

    st.plotly_chart(fig, use_container_width=True)

    st.info(
        "Esta superficie es ficticia. Se reemplazará "
        "por el modelo generado a partir de las mediciones."
    )

# RELLENO
elif pagina == "Relleno y materiales":
    st.title("Relleno y materiales")
    st.write("Configura una estimación preliminar.")

    material = st.selectbox(
        "Tipo de material",
        [
            "Tierra vegetal",
            "Tierra arcillosa",
            "Tierra limosa",
            "Tierra arenosa",
            "Material granular"
        ]
    )

    volumen = st.number_input(
        "Volumen calculado (m³)",
        min_value=0.0,
        value=1.0
    )

    factor = st.number_input(
        "Factor de volumen suelto",
        min_value=1.0,
        value=1.2,
        help="Valor de demostración, no una propiedad del material."
    )

    st.metric(
        "Volumen suelto estimado",
        f"{volumen * factor:.2f} m³"
    )
    st.caption(
        f"Material: {material}. El factor deberá calibrarse "
        "con propiedades reales del material."
    )

# PROYECTOS
elif pagina == "Mis proyectos":
    st.title("Mis proyectos")

    proyectos = st.session_state.proyectos

    if proyectos:
        st.dataframe(
            pd.DataFrame(proyectos),
            use_container_width=True
        )
    else:
        st.info("Crea tu primer proyecto para verlo aquí.")

# INFORMES
elif pagina == "Informes":
    st.title("Informes")
    st.write(
        "Aquí podrás preparar informes con las mediciones, "
        "el modelo 3D y el volumen de relleno."
    )
    st.info(
        "Exportación de informes pendiente de integrar."
    )
