import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ==========================================
# CONFIGURACIÓN
# ==========================================

st.set_page_config(
    page_title="Petroleum Production Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# CSS PROFESIONAL
# ==========================================

st.markdown("""
<style>

.main {
    background-color: #07111f;
}

[data-testid="stSidebar"] {
    background-color: #0b1f38;
}

.kpi-card{
    background-color:#0d2747;
    padding:15px;
    border-radius:15px;
    border:1px solid #1f4e79;
}

.kpi-title{
    color:#9cc7ff;
    font-size:14px;
}

.kpi-value{
    color:white;
    font-size:34px;
    font-weight:bold;
}

.block-container{
    padding-top:1rem;
}

hr{
    border-color:#1f4e79;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# CARGA DE DATOS
# ==========================================

@st.cache_data
def load_data():

    df = pd.read_csv("data/Prod2024.csv")

    for col in ["OilProd","GasProd","WaterProd"]:
        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        ).fillna(0)

    return df

df = load_data()

# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.title("FILTROS")

# Año

years = sorted(
    df["Year"].dropna().unique()
)

year = st.sidebar.selectbox(
    "Año",
    ["Todos"] + list(years)
)

if year != "Todos":
    df = df[df["Year"] == year]

# Campo

campos = sorted(
    df["Field"].dropna().unique()
)

campo = st.sidebar.selectbox(
    "Campo",
    ["Todos"] + list(campos)
)

if campo != "Todos":
    df = df[df["Field"] == campo]

# Condado

counties = sorted(
    df["County"].dropna().unique()
)

county = st.sidebar.selectbox(
    "Condado",
    ["Todos"] + list(counties)
)

if county != "Todos":
    df = df[df["County"] == county]

# Tipo pozo

tipos = sorted(
    df["Well_Typ"].dropna().unique()
)

tipo = st.sidebar.selectbox(
    "Tipo de Pozo",
    ["Todos"] + list(tipos)
)

if tipo != "Todos":
    df = df[df["Well_Typ"] == tipo]

# Estado

status = sorted(
    df["Wl_Status"].dropna().unique()
)

estado = st.sidebar.selectbox(
    "Estado del Pozo",
    ["Todos"] + list(status)
)

if estado != "Todos":
    df = df[df["Wl_Status"] == estado]

# Buscar pozo

pozo = st.sidebar.text_input(
    "Buscar Pozo"
)

if pozo:
    df = df[
        df["Well_Nm"].str.contains(
            pozo,
            case=False,
            na=False
        )
    ]

st.sidebar.markdown("---")

st.sidebar.subheader("INFORMACIÓN")

st.sidebar.metric(
    "Registros",
    f"{len(df):,}"
)

st.sidebar.metric(
    "Campos",
    df["Field"].nunique()
)

st.sidebar.metric(
    "Pozos",
    df["Well_Nm"].nunique()
   
)# ==========================================
# HEADER CON LOGO
# ==========================================

col_logo, col_titulo = st.columns([1,5], vertical_alignment="center")

with col_logo:
    st.image("logo_ipnesia.png", width=140)

with col_titulo:
    st.markdown("""
    # PETROLEUM PRODUCTION DASHBOARD

    ### Escuela Superior de Ingeniería y Arquitectura ESIA Ticomán

    **Docente:** Alvarado Bailey Omar

    **Alumnos**
    - Lara Araujo David Misael
    - Vargas López Efraín Ezequiel
    """)
st.markdown("---")
# ==========================================
# KPIs
# ==========================================

oil_total = df["OilProd"].sum()
gas_total = df["GasProd"].sum()
water_total = df["WaterProd"].sum()
pozos = df["Well_Nm"].nunique()

c1,c2,c3,c4 = st.columns(4)

c1.metric("Producción Petróleo", f"{oil_total:,.0f}")
c2.metric("Producción Gas", f"{gas_total:,.0f}")
c3.metric("Producción Agua", f"{water_total:,.0f}")
c4.metric("Número de Pozos", f"{pozos:,}")

st.markdown("---")

# ==========================================
# INDICADORES EJECUTIVOS
# ==========================================

campo_lider = (
    df.groupby("Field")["OilProd"]
    .sum()
    .idxmax()
)

pozo_lider = (
    df.groupby("Well_Nm")["OilProd"]
    .sum()
    .idxmax()
)

c5,c6 = st.columns(2)

c5.info(f"Campo Líder: {campo_lider}")
c6.info(f"Pozo Líder: {pozo_lider}")

# ==========================================
# FILA 1
# ==========================================

col1,col2 = st.columns(2)

with col1:

    field_prod = (
        df.groupby("Field")["OilProd"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig1 = px.bar(
        field_prod,
        x="Field",
        y="OilProd",
        color="OilProd",
        color_continuous_scale="Blues",
        title="Top 10 Campos Productores de Petróleo"
    )

    fig1.update_layout(
        plot_bgcolor="#0b1728",
        paper_bgcolor="#0b1728",
        font_color="white"
    )

    st.plotly_chart(fig1, use_container_width=True)

with col2:

    top_wells = (
        df.groupby("Well_Nm")["OilProd"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig2 = px.bar(
        top_wells,
        x="OilProd",
        y="Well_Nm",
        orientation="h",
        color="OilProd",
        color_continuous_scale="Teal",
        title="Top 10 Pozos Productores"
    )

    fig2.update_layout(
        plot_bgcolor="#0b1728",
        paper_bgcolor="#0b1728",
        font_color="white"
    )

    st.plotly_chart(fig2, use_container_width=True)

# ==========================================
# FILA 2
# ==========================================

col3,col4 = st.columns(2)

with col3:

    gas_prod = (
        df.groupby("Field")["GasProd"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig3 = px.bar(
        gas_prod,
        x="Field",
        y="GasProd",
        color="GasProd",
        color_continuous_scale="Greens",
        title="Producción de Gas"
    )

    fig3.update_layout(
        plot_bgcolor="#0b1728",
        paper_bgcolor="#0b1728",
        font_color="white"
    )

    st.plotly_chart(fig3, use_container_width=True)

with col4:

    water_prod = (
        df.groupby("Field")["WaterProd"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig4 = px.pie(
        water_prod,
        names="Field",
        values="WaterProd",
        hole=0.60,
        title="Distribución de Agua"
    )

    fig4.update_traces(
        marker=dict(
            colors=px.colors.sequential.Purples_r
        )
    )

    fig4.update_layout(
        paper_bgcolor="#0b1728",
        font_color="white"
    )

    st.plotly_chart(fig4, use_container_width=True)

# ==========================================
# WATER CUT
# ==========================================

st.markdown("## Water Cut por Campo")

watercut = (
    df.groupby("Field")[["OilProd","WaterProd"]]
    .sum()
    .reset_index()
)

watercut["WaterCut"] = (
    watercut["WaterProd"] /
    (watercut["OilProd"] + watercut["WaterProd"] + 1)
) * 100

fig_wc = px.bar(
    watercut.sort_values(
        "WaterCut",
        ascending=False
    ).head(15),
    x="Field",
    y="WaterCut",
    color="WaterCut",
    color_continuous_scale="Oranges",
    title="Water Cut (%)"
)

fig_wc.update_layout(
    plot_bgcolor="#0b1728",
    paper_bgcolor="#0b1728",
    font_color="white"
)

st.plotly_chart(fig_wc, use_container_width=True)

# ==========================================
# ESTADO DE POZOS
# ==========================================

status_df = (
    df.groupby("Wl_Status")
    .size()
    .reset_index(name="Cantidad")
)

fig_status = px.pie(
    status_df,
    names="Wl_Status",
    values="Cantidad",
    hole=0.60,
    title="Estado de Pozos"
)

fig_status.update_layout(
    paper_bgcolor="#0b1728",
    font_color="white"
)

st.plotly_chart(fig_status, use_container_width=True)

# ==========================================
# PRODUCCIÓN POR CONDADO
# ==========================================

county_prod = (
    df.groupby("County")["OilProd"]
    .sum()
    .sort_values(ascending=False)
    .head(15)
    .reset_index()
)

fig_county = px.bar(
    county_prod,
    x="County",
    y="OilProd",
    color="OilProd",
    color_continuous_scale="Cividis",
    title="Producción por Condado"
)

fig_county.update_layout(
    plot_bgcolor="#0b1728",
    paper_bgcolor="#0b1728",
    font_color="white"
)

st.plotly_chart(fig_county, use_container_width=True)

# ==========================================
# RESUMEN EJECUTIVO
# ==========================================

st.success(f'''
Campo líder: {campo_lider}

Pozo líder: {pozo_lider}

Producción Petróleo: {oil_total:,.0f}

Producción Gas: {gas_total:,.0f}

Producción Agua: {water_total:,.0f}
''')

# ==========================================
# BASE DE DATOS
# ==========================================

st.markdown("## Base de Datos")

st.dataframe(
    df,
    use_container_width=True,
    height=700,
    hide_index=True
)
