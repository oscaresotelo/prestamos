import streamlit as st
import sqlite3
import pandas as pd

# Conexión a la base de datos
conn = sqlite3.connect('financiera.db')
cursor = conn.cursor()

# Función para ejecutar consultas SQL y obtener resultados en un DataFrame
def run_query(query):
    cursor.execute(query)
    data = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    df = pd.DataFrame(data, columns=columns)
    return df

# Obtener valores únicos para el campo Nombre de la tabla Cobradores
cobradores_query = "SELECT IdCobrador, Nombre FROM Cobradores"
cobradores_data = run_query(cobradores_query)
cobradores_dict = dict(zip(cobradores_data['Nombre'], cobradores_data['IdCobrador']))

# Crear formulario para seleccionar fechas y Nombre de Cobrador
fecha_desde = st.date_input('Seleccionar fecha desde:')
fecha_hasta = st.date_input('Seleccionar fecha hasta:')

# Consulta SQL para obtener registros de la tabla Credito
query = f"""
SELECT Clientes.Nombre AS Cliente_Nombre, Clientes.Apellido AS Cliente_Apellido, 
       Credito.FechaAlta, Credito.TipoCredito, Credito.Capital, Credito.SaldoCapital, Cobradores.Nombre AS Cobrador_Nombre
FROM Credito
JOIN Clientes ON Credito.Dni = Clientes.Dni
JOIN Cobradores ON Credito.IdCobrador = Cobradores.IdCobrador
WHERE Credito.FechaAlta BETWEEN '{fecha_desde}' AND '{fecha_hasta}'
"""

# Ejecutar la consulta y mostrar resultados en un DataFrame
result_df = run_query(query)

# Agrupar por TipoCredito y calcular sumas y contar registros
grouped_df = result_df.groupby('TipoCredito').agg({'SaldoCapital': 'sum', 'Capital': 'sum', 'FechaAlta': 'size'}).reset_index()

# Renombrar la columna 'FechaAlta' a 'Cantidad_Registros'
grouped_df.rename(columns={'FechaAlta': 'Cantidad_Registros'}, inplace=True)

# Mostrar DataFrame agrupado en Streamlit
st.dataframe(grouped_df)

# Mostrar la cantidad de registros encontrados
st.write(f"Cantidad de registros encontrados: {len(result_df)}")

# Mostrar la suma del campo CuotaImporte
total_con_interes = grouped_df["SaldoCapital"].sum()
total_cuota_importe = grouped_df['Capital'].sum()
st.write(f"Capital Prestado: {total_cuota_importe}")
st.write(f'Total a Cobrar: {total_con_interes}')
st.write(f'Ganancia: {total_con_interes - total_cuota_importe}')
