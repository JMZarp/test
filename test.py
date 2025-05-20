import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt


st.title("Dashboard de Ventas - Supermercado")
st.markdown("""Este dashboard permite explorar ventas, ingresos y comportamiento de clientes en un supermercado ficticio. 
            Use los filtros a continuación para personalizar el análisis.
""")

st.subheader("🔍 Indicadores Clave (KPIs)")


df = pd.read_csv("data.csv")
#KPIs
total_ventas = df['Sales'].sum()
ingreso_bruto = df['gross income'].sum()
calificacion_prom = df['Rating'].mean()
facturas_totales = df['Invoice ID'].nunique()

col1, col2, col3, col4 = st.columns(4)
col1.metric("💵 Ventas Totales", f"${total_ventas:,.2f}")
col2.metric("💰 Ingreso Bruto", f"${ingreso_bruto:,.2f}")
col3.metric("⭐ Calificación Promedio", f"{calificacion_prom:.2f}")
col4.metric("🧾 Total de Facturas", f"{facturas_totales}")

df.columns = df.columns.str.strip()
df = df.rename(columns={"Sales": "Total"})  #Se cambia el nombre a Total para mejor lectura
df["Date"] = pd.to_datetime(df["Date"])

#Sidebar para filtro
st.sidebar.header("Filtros")
branch = st.sidebar.multiselect("Seleccionar sucursal", df["Branch"].unique(), default=df["Branch"].unique())
product_lines = st.sidebar.multiselect("Seleccionar líneas de producto", df["Product line"].unique(), default=df["Product line"].unique())

df_filtered = df[(df["Branch"].isin(branch)) & (df["Product line"].isin(product_lines))]

#1. Evolución de las Ventas Totales
st.subheader("🗓️ Evolución de Ventas Totales")
ventas_diarias = df_filtered.groupby("Date")["Total"].sum().reset_index()
fig1 = px.line(ventas_diarias, x="Date", y="Total", title="Ventas Totales por Día")
st.plotly_chart(fig1, use_container_width=True)
st.markdown("📈 Este gráfico muestra cómo evolucionaron las ventas diarias. Permite detectar picos de ventas o caídas según el día.")


#2. Ingresos por Línea de Producto
st.subheader("📦 Ingresos por Línea de Producto")
ventas_producto = df_filtered.groupby("Product line")["Total"].sum().sort_values().reset_index()
fig2 = px.bar(ventas_producto, x="Total", y="Product line", orientation='h', title="Ventas por Línea de Producto")
st.plotly_chart(fig2, use_container_width=True)
st.markdown("📊 Compara los ingresos generados por cada línea de producto. Útil para identificar los productos más rentables.")

#3. Distribución de la Calificación de Clientes
st.subheader("⭐ Distribución de Calificaciones de Clientes")
fig3 = px.histogram(df_filtered, x="Rating", nbins=20, title="Distribución de Calificaciones")
st.plotly_chart(fig3, use_container_width=True)
st.markdown("⭐ Este histograma revela cómo se distribuyen las calificaciones de los clientes. Una buena calificación promedio indica satisfacción.")

#4. Comparación del Gasto por Tipo de Cliente
st.subheader("👥 Comparación del Gasto por Tipo de Cliente")
fig4 = px.box(df_filtered, x="Customer type", y="Total", color="Customer type", title="Distribución del Gasto por Tipo de Cliente")
st.plotly_chart(fig4, use_container_width=True)
st.markdown("🧍‍♂️ Este boxplot compara el gasto total entre clientes 'Member' y 'Normal'. Ayuda a entender patrones de consumo.")

#5. Relación entre Costo y Ganancia Bruta
st.subheader("💰 Relación entre Costo y Ganancia Bruta")
fig5 = px.scatter(df_filtered, x="cogs", y="gross income", color="Product line", title="Costo vs. Ingreso Bruto")
st.plotly_chart(fig5, use_container_width=True)
st.markdown("💹 El scatterplot muestra una clara relación positiva entre el costo de bienes vendidos (`cogs`) y el ingreso bruto.")

#6. Métodos de Pago Preferidos
st.subheader("💳 Métodos de Pago Preferidos")
pago = df_filtered["Payment"].value_counts().reset_index()
pago.columns = ["Método", "Cantidad"]
fig6 = px.pie(pago, names="Método", values="Cantidad", title="Métodos de Pago Utilizados")
st.plotly_chart(fig6, use_container_width=True)
st.markdown("💳 Aquí se visualizan los métodos de pago más frecuentes entre los clientes.")

#7. Análisis de Correlación Numérica
st.subheader("📈 Matriz de Correlación")
cols_corr = ["Unit price", "Quantity", "Tax 5%", "Total", "cogs", "gross income", "Rating"]
fig7, ax = plt.subplots()
sns.heatmap(df_filtered[cols_corr].corr(), annot=True, cmap="coolwarm", ax=ax)
st.pyplot(fig7)
st.markdown("🔍 Este mapa de calor muestra la correlación entre variables numéricas. Es útil para detectar relaciones lineales fuertes.")

#8. Ingreso Bruto por Sucursal y Línea de Producto
st.subheader("🏪 Ingreso Bruto por Sucursal y Línea de Producto")
pivot = df_filtered.pivot_table(index="Branch", columns="Product line", values="gross income", aggfunc="sum", fill_value=0)
fig8 = px.imshow(pivot, text_auto=True, title="Ingreso Bruto por Sucursal y Producto", labels=dict(color="Ingreso"))
st.plotly_chart(fig8, use_container_width=True)
st.markdown("🏬 Este heatmap revela qué líneas de producto generan más ingreso bruto en cada sucursal.")

#9. Visualización en 3D
st.subheader("🧊 Visualización 3D: Precio Unitario, Cantidad y Ventas Totales")
st.markdown("Esta visualización permite observar cómo la combinación del precio y la cantidad impacta las ventas. Colores indican la línea de producto.")
fig9 = px.scatter_3d(df_filtered, 
                     x='Unit price', 
                     y='Quantity', 
                     z='Total', 
                     color='Product line',
                     opacity=0.7,
                     title='Relación 3D: Unit Price vs Quantity vs Total')
st.plotly_chart(fig9, use_container_width=True)


