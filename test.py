# ------------------------
# 📦 Importación de librerías
# ------------------------
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D

# ------------------------
# 📁 Cargar el conjunto de datos
# ------------------------
df = pd.read_csv("SuperMarket Analysis.csv")
df['Date'] = pd.to_datetime(df['Date'])  # Convertimos la columna Date a datetime
df['Hour'] = pd.to_datetime(df['Time']).dt.hour  # Extraemos la hora de la columna Time

# ------------------------
# 🏷️ Título general
# ------------------------
st.title("Dashboard de Análisis de Ventas de Supermercado")
st.markdown("Este dashboard presenta un análisis exploratorio interactivo de ventas, productos y comportamiento de clientes.")

# =========================================================================
# 🧮 1. Visualización básica de datos
# =========================================================================
st.header("1. Visualización básica de datos")

# 🟦 Línea de ventas diarias
st.subheader("Ventas diarias")
daily_sales = df.groupby('Date')['Sales'].sum()
fig1, ax1 = plt.subplots()
ax1.plot(daily_sales.index, daily_sales.values, marker='o', color='royalblue')
ax1.set_xlabel('Fecha')
ax1.set_ylabel('Ventas ($)')
st.pyplot(fig1)

# 🔵 Dispersión: Precio unitario vs Cantidad
st.subheader("Precio unitario vs. Cantidad por línea de producto")
fig2, ax2 = plt.subplots()
sns.scatterplot(data=df, x='Unit price', y='Quantity', hue='Product line', ax=ax2)
st.pyplot(fig2)

# 📦 Boxplot de ingresos brutos por ciudad
st.subheader("Distribución de ingresos brutos por ciudad")
fig3, ax3 = plt.subplots()
sns.boxplot(data=df, x='City', y='gross income', ax=ax3)
st.pyplot(fig3)

# =========================================================================
# 📊 2. Visualizaciones compuestas
# =========================================================================
st.header("2. Visualizaciones compuestas")

# 🕒 Ventas por hora del día según tipo de cliente
st.subheader("Ventas por hora del día según tipo de cliente")
hourly_sales = df.groupby(['Hour', 'Customer type'])['Sales'].sum().reset_index()
fig4, ax4 = plt.subplots()
sns.lineplot(data=hourly_sales, x='Hour', y='Sales', hue='Customer type', marker="o", ax=ax4)
st.pyplot(fig4)

# 🔥 Heatmap: ventas por ciudad y método de pago
st.subheader("Total de ventas por ciudad y método de pago")
pivot_heatmap = df.pivot_table(values='Sales', index='City', columns='Payment', aggfunc='sum')
fig5, ax5 = plt.subplots()
sns.heatmap(pivot_heatmap, annot=True, fmt=".0f", cmap="YlGnBu", ax=ax5)
st.pyplot(fig5)

# =========================================================================
# 🔺 3. Visualización en 3D
# =========================================================================
st.header("3. Visualización en 3D")

st.markdown("Explora la relación entre el **precio unitario**, la **cantidad vendida** y el **total de ventas**.")

fig6 = plt.figure(figsize=(8, 6))
ax6 = fig6.add_subplot(111, projection='3d')
ax6.scatter(df['Unit price'], df['Quantity'], df['Sales'], c='tomato', alpha=0.6)
ax6.set_xlabel('Unit Price')
ax6.set_ylabel('Quantity')
ax6.set_zlabel('Sales')
ax6.set_title('3D: Precio unitario vs Cantidad vs Ventas')
st.pyplot(fig6)

# =========================================================================
# 💬 4. Reflexión final
# =========================================================================
st.header("Reflexión final")
st.markdown("""
Este dashboard interactivo facilita la exploración de patrones clave en las ventas:
- Comparación entre ciudades, líneas de productos y tipos de clientes.
- Identificación de horas pico.
- Relación entre variables críticas como precio, cantidad y ventas.

Estas herramientas ayudan a la toma de decisiones estratégicas basadas en datos.
""")
