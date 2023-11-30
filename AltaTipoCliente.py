import streamlit as st
import sqlite3

# Conexión a la base de datos SQLite
conn = sqlite3.connect('financiera.db')
cursor = conn.cursor()
if "ingreso" not in st.session_state:
    st.session_state.ingreso = ""

if st.session_state.ingreso == "":
    st.warning("Por favor Ingrese Correctamente")
else:
    def local_css(file_name):
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    local_css("estilos.css")

    # Crear la tabla TipoClientes si no existe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS TipoClientes (
            IdTipoCliente INTEGER PRIMARY KEY AUTOINCREMENT,
            Nombre TEXT,
            Activo BOOLEAN
        )
    ''')
    conn.commit()

    # Función para insertar datos en la tabla
    def insertar_datos(nombre, activo):
        cursor.execute('INSERT INTO TipoClientes (Nombre, Activo) VALUES (?, ?)', (nombre, activo))
        conn.commit()

    # Función para mostrar el formulario
    def formulario_ingreso_datos():
        st.header('Tipos de Clientes')

        # Campo Nombre
        nombre = st.text_input('Nombre')

        # Campo Activo
        activo = st.checkbox('Activo')

        # Botón para enviar los datos
        if st.button('Guardar'):
            insertar_datos(nombre, activo)
            st.success('Datos guardados correctamente.')

    # Mostrar el formulario
    formulario_ingreso_datos()
