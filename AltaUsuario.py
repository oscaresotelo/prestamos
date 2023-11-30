import streamlit as st
import sqlite3
import pandas as pd



tab1 , tab2 = st.tabs(['Alta de Usuarios','Desactivar Usuarios'])
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
local_css("estilos.css")

if "ingreso" not in st.session_state:
    st.session_state.ingreso = ""

if st.session_state.ingreso == "":
    st.warning("Por favor Ingrese Correctamente")
else:
    # Conectar a la base de datos SQLite
    conn = sqlite3.connect('financiera.db')
    cursor = conn.cursor()

    # Crear la tabla Cobradores si no existe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS "Cobradores" (
            "IdCobrador"    INT,
            "Nombre"        TEXT,
            "Zona"          TEXT,
            "Activo"        NUM,
            "Tipo"          INTEGER
        );
    ''')
    conn.commit()

    # Función para insertar datos en la tabla Cobradores
    def insertar_datos(id_cobrador, nombre, zona, activo, tipo,dni, logpas):
        cursor.execute('''
            INSERT INTO Cobradores (IdCobrador, Nombre,  Zona, Activo, Tipo, Dni, Pass)
            VALUES (?, ?, ?, ?, ?,?,?);
        ''', (id_cobrador, nombre, zona, activo, tipo, dni , logpas))
        conn.commit()

    # Función para obtener todos los datos de la tabla Cobradores
    def obtener_todos_los_datos():
        cursor.execute('SELECT * FROM Cobradores;')
        return cursor.fetchall()

    # Función para actualizar el estado Activo de un registro
    def actualizar_estado_activo(id_cobrador, nuevo_estado):
        cursor.execute('''
            UPDATE Cobradores
            SET Activo = ?
            WHERE IdCobrador = ?;
        ''', (nuevo_estado, id_cobrador))
        conn.commit()

    # Función para obtener la lista de tipos (1: Administrador, 2: Cobrador)
    def obtener_lista_tipos():
        return {
            1: "Administrador",
            2: "Cobrador"
        }

    # Función para mapear valores de Activo a texto
    def mapear_estado_activo(valor):
        return "Activo" if valor == 1 else "Inactivo"

    # Streamlit App
    with tab1:

        st.title('Alta Y de Usuarios')

        # Campos del formulario
        id_cobrador = st.number_input('IdCobrador', min_value=1)
        dni =  st.number_input('Dni', min_value=1)
        nombre = st.text_input('Nombre')
        logpas = st.text_input('Contraseña')
        zona = st.text_input('Zona')
        activo = st.checkbox('Activo')
        tipo = st.selectbox('Tipo', options=list(obtener_lista_tipos().values()))

        # Botón para ingresar los datos en la tabla Cobradores
        if st.button('Ingresar Datos'):
            activo = 1 if activo else 0  # Convertir a 1 si está activo, 0 si no
            tipo_id = list(obtener_lista_tipos().keys())[list(obtener_lista_tipos().values()).index(tipo)]
            insertar_datos(id_cobrador, nombre, zona, activo, tipo_id,dni, logpas)
            st.success('Datos ingresados correctamente.')
    with tab2:
        # Mostrar datos en un DataFrame
        datos_cobradores = obtener_todos_los_datos()
        df_cobradores = pd.DataFrame(datos_cobradores, columns=['IdCobrador', 'Nombre','Zona', 'Activo', 'Tipo','Dni' ,'Pass',])
        df_cobradores['Activo'] = df_cobradores['Activo'].map(mapear_estado_activo)  # Mapear valores de Activo a texto
        st.write('**Datos de Cobradores:**')
        st.dataframe(df_cobradores)

        # Sección para cambiar el estado Activo
        selected_id = st.number_input('Ingrese IdCobrador para cambiar estado Activo', min_value=1)

        if st.button('Cambiar Estado '):
            nuevo_estado = 1 if df_cobradores.loc[df_cobradores['IdCobrador'] == selected_id, 'Activo'].values[0] == 0 else 0
            actualizar_estado_activo(selected_id, nuevo_estado)
            st.success(f'Estado Actualizado {selected_id}.')

    # Cerrar la conexión a la base de datos al finalizar la aplicación
    conn.close()
