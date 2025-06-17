import streamlit as st
import pandas as pd

# Función para cargar y cachear datos desde el CSV público de Google Sheets
@st.cache_data
def cargar_datos():
    url_csv_publico = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQAW1sJnr1Nfsxa_n0f7qo19ru4WDhKrjnxhd21IrhVuS19M4PENvoeFcZCrAVPtV68ej6vP1DKfewo/pub?output=csv"
    df = pd.read_csv(url_csv_publico)
    return df

st.title("Comparativo de Celulares")

# Cargar datos
df = cargar_datos()

# --- FILTROS ---

# Filtro por País
if "País" in df.columns:
    paises = df["País"].dropna().unique()
    pais_seleccionado = st.selectbox("Filtrar por País", ["Todos"] + list(sorted(paises)))
else:
    pais_seleccionado = "Todos"

# Filtro por Cliente
if "Cliente" in df.columns:
    clientes = df["Cliente"].dropna().unique()
    cliente_seleccionado = st.selectbox("Filtrar por Cliente", ["Todos"] + list(sorted(clientes)))
else:
    cliente_seleccionado = "Todos"

# Filtrar dataframe por país y cliente
df_filtrado = df.copy()
if pais_seleccionado != "Todos":
    df_filtrado = df_filtrado[df_filtrado["País"] == pais_seleccionado]
if cliente_seleccionado != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Cliente"] == cliente_seleccionado]

# Filtro múltiple para Marcas (hasta 5)
if "Marca" in df_filtrado.columns:
    marcas = df_filtrado["Marca"].dropna().unique()
    marcas_seleccionadas = st.multiselect(
        "Selecciona hasta 5 Marcas",
        options=sorted(marcas),
        default=list(sorted(marcas))[:5],
    )
    # Limitar manualmente a 5 marcas
    if len(marcas_seleccionadas) > 5:
        st.warning("Por favor selecciona máximo 5 marcas.")
        marcas_seleccionadas = marcas_seleccionadas[:5]
    if marcas_seleccionadas:
        df_filtrado = df_filtrado[df_filtrado["Marca"].isin(marcas_seleccionadas)]

# Filtro múltiple para Modelos (hasta 10)
if "Modelo" in df_filtrado.columns:
    modelos = df_filtrado["Modelo"].dropna().unique()
    modelos_seleccionados = st.multiselect(
        "Selecciona hasta 10 Modelos",
        options=sorted(modelos),
        default=list(sorted(modelos))[:10],
    )
    # Limitar manualmente a 10 modelos
    if len(modelos_seleccionados) > 10:
        st.warning("Por favor selecciona máximo 10 modelos.")
        modelos_seleccionados = modelos_seleccionados[:10]
    if modelos_seleccionados:
        df_filtrado = df_filtrado[df_filtrado["Modelo"].isin(modelos_seleccionados)]

# Columnas en el orden EXACTO solicitado
columnas_ordenadas = [
    "País", "Cliente", "Marca", "Modelo", "Pantalla", "Procesador", "RAM",
    "Almacenamiento", "Cámara", "Batería", "Certificación", "Sistema Operativo",
    "Precio", "Precio promoción"
]

# Selecciona solo las columnas que existen realmente en el DataFrame y en ese orden
columnas_finales = [col for col in columnas_ordenadas if col in df_filtrado.columns]

st.write(f"### Resultados ({len(df_filtrado)})")

# Mostrar la tabla con las columnas ordenadas
st.dataframe(df_filtrado[columnas_finales].reset_index(drop=True))
