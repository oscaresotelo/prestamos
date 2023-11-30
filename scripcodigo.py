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
cobrador_seleccionado_nombre = st.selectbox('Seleccionar Nombre de Cobrador:', cobradores_dict.keys())
cobrador_seleccionado_id = cobradores_dict[cobrador_seleccionado_nombre]

# Consulta SQL para obtener registros de la tabla DetalleCredito
query = f"""
SELECT Clientes.Nombre AS Cliente_Nombre, Clientes.Apellido AS Cliente_Apellido, 
       DetalleCredito.FechaVto, DetalleCredito.CuotaImporte, Cobradores.Nombre AS Cobrador_Nombre
FROM DetalleCredito
JOIN Credito ON DetalleCredito.IdCredito = Credito.IdCredito
JOIN Clientes ON Credito.Dni = Clientes.Dni
JOIN Cobradores ON Credito.IdCobrador = Cobradores.IdCobrador
WHERE DetalleCredito.FechaVto BETWEEN '{fecha_desde}' AND '{fecha_hasta}'
      AND Cobradores.IdCobrador = {cobrador_seleccionado_id}
"""

# Ejecutar la consulta y mostrar resultados en un DataFrame
result_df = run_query(query)

# Mostrar DataFrame en Streamlit
st.dataframe(result_df)

# Mostrar la cantidad de registros encontrados
st.write(f"Cantidad de registros encontrados: {len(result_df)}")

# Mostrar la suma del campo CuotaImporte
total_cuota_importe = result_df['CuotaImporte'].sum()
st.write(f"Suma del campo CuotaImporte: {total_cuota_importe}")
