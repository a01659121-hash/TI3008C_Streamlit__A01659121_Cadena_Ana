import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(
    page_title="Explorador de operación",
    page_icon="📊",
    layout="wide",
)


@st.cache_data
def cargar_datos() -> pd.DataFrame:
    """Carga los datos que utilizará la aplicación."""
    datos = pd.read_csv("datos_ejemplo.csv")
    datos["Fecha"] = pd.to_datetime(datos["Fecha"])
    return datos


df = cargar_datos()

st.title("Explorador de operación")
st.caption("Aplicación inicial para explorar resultados por área y región.")

# TODO OBLIGATORIO: escribe tu nombre completo.
st.write("**Desarrollado por:** Ana Lucía Cadena Castellanos")

st.sidebar.header("Filtros")

areas_disponibles = sorted(df["Área"].unique())
areas_seleccionadas = st.sidebar.multiselect(
    "Área",
    options=areas_disponibles,
    default=areas_disponibles,
)

df_filtrado = df[df["Área"].isin(areas_seleccionadas)].copy()

st.subheader("Datos disponibles")
st.dataframe(df_filtrado, width="stretch", hide_index=True)

casos_por_fecha = (
    df_filtrado.groupby("Fecha", as_index=False)["Casos"]
    .sum()
    .sort_values("Fecha")
)

fig = px.line(
    casos_por_fecha,
    x="Fecha",
    y="Casos",
    markers=True,
    title="Casos por fecha",
)
st.plotly_chart(fig, width="stretch")

st.info(
    "Esta es la versión inicial. Selecciona una opción de la actividad y agrega "
    "una mejora funcional para el usuario."
)


# ================================================================
# ZONA DE TRABAJO
# Implementa UNA de las opciones indicadas en INSTRUCCIONES_ACTIVIDAD.md.
# Puedes reorganizar el código existente cuando sea necesario.
# ================================================================

# TODO OPCIÓN A: Tablero ejecutivo
# - Agrega al menos dos indicadores con st.metric.
# - Incorpora otro filtro.
# - Organiza dos vistas mediante st.tabs.

# TODO OPCIÓN B: Explorador de datos
# - Permite cargar un CSV con st.file_uploader.
# - Valida que el archivo tenga las columnas necesarias.
# - Permite descargar df_filtrado con st.download_button.

# --- PARTE 5: MEJORA FUNCIONAL - OPCIÓN B: EXPLORADOR DE DATOS ---
st.divider()
st.subheader("📂 Explorador y Análisis de Datos Personalizado")
st.write("Sube tu propio archivo CSV para explorar, filtrar y descargar los resultados en tiempo real.")

# 1. Carga de archivos CSV mediante st.file_uploader
archivo_subido = st.file_uploader("Sube un archivo CSV con tus datos", type=["csv"])

if archivo_subido is not None:
    import pandas as pd
    try:
        # Leer el archivo CSV
        df_usuario = pd.read_csv(archivo_subido)
        
        # 2. Validación de columnas necesarias (ejemplo: validamos que tenga al menos 2 columnas)
        if len(df_usuario.columns) < 2:
            st.error("El archivo CSV debe contener al menos dos columnas para realizar el análisis.")
        else:
            st.success("¡Archivo cargado y validado exitosamente!")
            
            # Mostrar vista previa de las columnas detectadas
            st.write(f"Columnas detectadas: {list(df_usuario.columns)}")
            
            # Filtro opcional interactivo basado en la columna seleccionada
            columna_filtro = st.selectbox("Selecciona una columna para filtrar (opcional):", options=df_usuario.columns)
            valores_unicos = df_usuario[columna_filtro].unique()
            valor_seleccionado = st.multiselect(f"Filtrar valores en {columna_filtro}:", options=valores_unicos, default=list(valores_unicos))
            
            # Filtrar el DataFrame
            df_filtrado = df_usuario[df_usuario[columna_filtro].isin(valor_seleccionado)]
            
            # 3. Visualización mediante st.dataframe
            st.write(f"Mostrando {len(df_filtrado)} registros filtrados:")
            st.dataframe(df_filtrado, use_container_width=True)
            
            # 4. Descarga de los datos filtrados mediante st.download_button
            csv_convertido = df_filtrado.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Descargar datos filtrados (CSV)",
                data=csv_convertido,
                file_name="datos_filtrados.csv",
                mime="text/csv",
            )
            
    except Exception as e:
        st.error(f"Ocurrió un error al procesar el archivo: {e}")
else:
    st.info("Esperando a que subas un archivo CSV para comenzar la exploración...")

# TODO OPCIÓN C: Simulador
# - Solicita al menos dos valores al usuario.
# - Realiza un cálculo con esos valores.
# - Muestra un resultado y un mensaje success, warning o error.

# TODO OPCIÓN D: Reporte interactivo
# - Agrega una introducción que explique el propósito.
# - Organiza resultados y metodología en pestañas o en la barra lateral.
# - Incluye una conclusión o recomendación basada en los datos visibles.

