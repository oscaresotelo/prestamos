import streamlit as st
import sqlite3
import pandas as pd

# Conexión a la base de datos
conn = sqlite3.connect('financiera.db')
cursor = conn.cursor()

# Función para obtener los datos de DetalleCredito y Cobradores
def obtener_datos(fecha, nombre_cobrador):
    query = f'''
    SELECT Cobradores.Nombre, DetalleCredito.*
    FROM DetalleCredito
    JOIN Cobradores ON DetalleCredito.IdCobrador = Cobradores.IdCobrador
    WHERE DetalleCredito.FechaPago = '{fecha}' AND Cobradores.Nombre = '{nombre_cobrador}'
    '''
    cursor.execute(query)
    data = cursor.fetchall()
    column_names = [description[0] for description in cursor.description]
    df = pd.DataFrame(data, columns=column_names)
    return df

# Interfaz web con Streamlit
st.title('Rendicion de Pagos')

# Formulario para ingresar la fecha
fecha_elegida = st.date_input('Seleccione una fecha')

# Obtener la lista de nombres de cobradores
nombres_cobradores = [nombre[0] for nombre in cursor.execute('SELECT DISTINCT Nombre FROM Cobradores').fetchall()]

# Dropdown para seleccionar el nombre del cobrador
nombre_cobrador_elegido = st.selectbox('Seleccione el nombre del cobrador', nombres_cobradores)

# Botón para realizar la búsqueda
if st.button('Buscar'):
    # Obtener los datos
    df_resultado = obtener_datos(str(fecha_elegida), nombre_cobrador_elegido)

    # Mostrar los resultados
    st.write('Resultados:')
    st.write(df_resultado)

# Cerrar la conexión a la base de datos al finalizar
conn.close()
