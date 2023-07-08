import pandas as pd
import plotly.express as px
import streamlit as st
nombre_logo = "estela.png"

st.set_page_config(page_title="Gastos Dashboard",
                   page_icon=":money_with_wings:",
                   layout="wide")


df = pd.read_excel("gastos_2020.xlsx")

#-----side bar-----
st.sidebar.title("Estela Santacruz & Asociados")
st.sidebar.image(nombre_logo, use_column_width=True)
st.sidebar.header("Filtre aqui")
TIPO = st.sidebar.selectbox("Compras o ventas?", options=df["TIPO"].unique())
df_selection = df.query("TIPO == @TIPO")

st.title("Registros a la fecha:")
st.dataframe(df_selection)
st.title(f":bar_chart: Dashboard de {TIPO}")
st.markdown("##")

# ---- KPI ------
total = int(df_selection["TOTAL"].sum())
promedio_por_total = round(df_selection["TOTAL"].mean(), 2)
cantidad_registros = df_selection.shape[0]
left_column, midle_column, rigth_column = st.columns(3)
with left_column:
    st.subheader(f"Total {TIPO}")
    st.subheader(f"Gs {total:,}")
with midle_column:
    st.subheader("Promedio del total:")
    st.subheader(f"Gs {promedio_por_total:,}")
with rigth_column:
    st.subheader("Cantidad de registros:")
    st.subheader(f"{cantidad_registros}")

# Calculos de la DF

# Crear DataFrame para ventas
df_ventas = df[df["TIPO"] == "VENTA"]
ventas = df_ventas.groupby("CONCEPTO")["TOTAL"].sum()

# Crear DataFrame para gastos
df_gastos = df[df["TIPO"] == "GASTO"]
gastos = df_gastos.groupby("CONCEPTO")["TOTAL"].sum()

# Mostrar gráfico según el valor de df_selection
if "VENTA" in df_selection["TIPO"].values:
    fig = px.pie(values=ventas, names=ventas.index, title="Ventas por concepto")
elif "GASTO" in df_selection["TIPO"].values:
    fig = px.pie(values=gastos, names=gastos.index, title="Gastos por concepto")

# Mostrar gráfico en Streamlit
st.plotly_chart(fig)
#Ocultar los signos por defecto de la pagina
hide_st_style = """
<style>
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }
</style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)
