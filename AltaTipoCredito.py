# import streamlit as st
# import sqlite3
# import pandas as pd

# # Conexión a la base de datos SQLite
# conn = sqlite3.connect('financiera.db')
# cursor = conn.cursor()

# # Crear la tabla si no existe
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS TipoPrestamo (
#         Id INTEGER PRIMARY KEY AUTOINCREMENT,
#         Nombre TEXT,
#         CantCuotas INT,
#         Interes INT,
#         Activo NUM,
#         TipoCredito TEXT,
#         TipoCobro TEXT
#     )
# ''')
# conn.commit()

# # Crear formulario para ingresar datos a la tabla
# st.title('Crear Tipo de Credito')

# nombre = st.text_input('Nombre del Credito:')
# cant_cuotas = st.number_input('Cantidad de cuotas:', min_value=1, value=1)
# interes = st.number_input('Tasa de interés (%):', min_value=0, value=0)
# activo = st.checkbox('Activo')

# tipo_credito = st.selectbox('Tipo de Crédito:', ['COMERCIAL', 'PERSONAL'])
# tipo_cobro = st.selectbox('Tipo de Cobro:', ['SEMANAL', 'MENSUAL'])

# if st.button('Guardar'):
#     # Insertar datos en la tabla (Id no se incluye ya que es autoincremental)
#     cursor.execute('''
#         INSERT INTO TipoPrestamo (Nombre, CantCuotas, Interes, Activo, TipoCredito, TipoCobro)
#         VALUES (?, ?, ?, ?, ?, ?)
#     ''', (nombre, cant_cuotas, interes, 1 if activo else 0, tipo_credito, tipo_cobro))
    
#     conn.commit()
#     st.success('Datos guardados exitosamente!')

# # Mostrar los registros donde el valor del campo Activo es igual a 1
# st.title('Registros Activos')
# query = "SELECT * FROM TipoPrestamo WHERE Activo = 1"
# result = cursor.execute(query).fetchall()

# # Crear un DataFrame con los resultados
# columns = [description[0] for description in cursor.description]
# df = pd.DataFrame(result, columns=columns)

# # Mostrar el DataFrame
# st.dataframe(df)

# # Cerrar la conexión a la base de datos
# conn.close()
import streamlit as st
import sqlite3
import pandas as pd

tab1 , tab2 = st.tabs(['Nueva Linea Credito','Desactivar Linea Credito'])

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
local_css("estilos.css")

if "ingreso" not in st.session_state:
    st.session_state.ingreso = ""

if st.session_state.ingreso == "":
    st.warning("Por favor Ingrese Correctamente")
else:
    # Conexión a la base de datos SQLite
    conn = sqlite3.connect('financiera.db')
    cursor = conn.cursor()

    # Crear la tabla si no existe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS TipoPrestamo (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Nombre TEXT,
            CantCuotas INT,
            Interes INT,
            Activo NUM,
            TipoCredito TEXT,
            TipoCobro TEXT
        )
    ''')
    conn.commit()

    # Crear formulario para ingresar datos a la tabla
    with tab1:
        st.title('Crear Tipo de Crédito')

        nombre = st.text_input('Nombre del Crédito:')
        cant_cuotas = st.number_input('Cantidad de cuotas:', min_value=1, value=1)
        interes = st.number_input('Tasa de interés (%):', min_value=0, value=0)
        activo = st.checkbox('Activo')

        tipo_credito = st.selectbox('Tipo de Crédito:', ['COMERCIAL', 'PERSONAL'])
        tipo_cobro = st.selectbox('Tipo de Cobro:', ['SEMANAL', 'MENSUAL'])

        if st.button('Guardar'):
            # Insertar datos en la tabla (Id no se incluye ya que es autoincremental)
            cursor.execute('''
                INSERT INTO TipoPrestamo (Nombre, CantCuotas, Interes, Activo, TipoCredito, TipoCobro)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (nombre, cant_cuotas, interes, 1 if activo else 0, tipo_credito, tipo_cobro))
            
            conn.commit()
            st.success('Datos guardados exitosamente!')

        # Mostrar los registros donde el valor del campo Activo es igual a 1
    with tab2:
        st.title('Creditos Activos')
        query = "SELECT * FROM TipoPrestamo WHERE Activo = 1"
        result = cursor.execute(query).fetchall()

        # Crear un DataFrame con los resultados
        columns = [description[0] for description in cursor.description]
        df = pd.DataFrame(result, columns=columns)

        # Agregar la posibilidad de seleccionar créditos y cambiar el campo Activo
        selected_rows = st.multiselect('Seleccionar créditos:', df['Id'].tolist())

        if st.button('Cambiar Estado a Inactivo'):
            for row_id in selected_rows:
                cursor.execute("UPDATE TipoPrestamo SET Activo = 0 WHERE Id = ?", (row_id,))
            conn.commit()
            st.success('Estado cambiado exitosamente!')

        # Mostrar el DataFrame actualizado
        st.dataframe(df)

        # Cerrar la conexión a la base de datos
        conn.close()
