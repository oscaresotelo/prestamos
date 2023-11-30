
import streamlit as st
import sqlite3
from st_pages import Page, show_pages, add_page_title
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
            Activo TEXT
        )
    ''')
    conn.commit()

    # Crear la tabla Clientes si no existe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Clientes (
            IdClientes INTEGER PRIMARY KEY AUTOINCREMENT,
            TipoCliente INTEGER,
            Dni INTEGER,
            Nombre TEXT,
            Apellido TEXT,
            Direccion TEXT,
            Observacion TEXT
        )
    ''')
    conn.commit()

    # Función para insertar datos en la tabla TipoClientes
    def insertar_tipo_cliente(nombre, activo):
        cursor.execute('''
            INSERT INTO TipoClientes (Nombre, Activo)
            VALUES (?, ?)
        ''', (nombre, activo))
        conn.commit()

    # Función para insertar datos en la tabla Clientes
    def insertar_cliente(tipo_cliente, dni, nombre, apellido, telefono, direccion, observacion):
        cursor.execute('''
            INSERT INTO Clientes (TipoCliente, Dni, Nombre, Apellido, Telefono, Direccion, Observacion)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (tipo_cliente, dni, nombre, apellido, telefono, direccion, observacion))
        conn.commit()

    # Página principal de Streamlit
    def main():
        # show_pages([
        #         Page("Altaclientes.py", "Alta De Clientes"),
        #         Page("AltaCreditos.py", "Alta De Creditos"),
        #         Page("AltaTipoCliente.py", "Alta Tipo Cliente"),
        #         Page("AltaTipoCredito.py", "Alta Tipo Credito"),
        #         Page("ConsultaCredito.py", "Consulta de Creditos"),
        #         Page("AltaUsuario.py", "Alta Modificacion Usuarios"),
               
        #         Page("prubalink.py", "Cobranza"),
                
        #     ])
       
        # Formulario para ingresar datos del tipo de cliente
        # nombre_tipo_cliente = st.text_input('Nombre Tipo de Cliente')
        # activo_tipo_cliente = st.text_input('Activo Tipo de Cliente')
        # if st.button('Guardar Tipo de Cliente'):
        #     insertar_tipo_cliente(nombre_tipo_cliente, activo_tipo_cliente)
        #     st.success('Tipo de Cliente guardado exitosamente!')

        # Formulario para ingresar datos del cliente
        st.title('Ingresar Clientes')
        tipo_clientes = cursor.execute('SELECT IdTipoCliente, Nombre FROM TipoClientes').fetchall()
        tipo_cliente_names = [tc[1] for tc in tipo_clientes]
        tipo_cliente = st.selectbox('Seleccionar Tipo de Cliente', tipo_cliente_names)

        dni = st.number_input('DNI', min_value=0)
        nombre = st.text_input('Nombre')
        apellido = st.text_input('Apellido')
        direccion = st.text_input('Dirección')
        telefono = st.number_input("Telefono",min_value= 0)
        observacion = st.text_area('Observación')

        # Botón para insertar datos en la base de datos
        if st.button('Grabar Cliente'):
            tipo_cliente_id = tipo_clientes[tipo_cliente_names.index(tipo_cliente)][0]
            insertar_cliente(tipo_cliente_id, dni, nombre, apellido, telefono,direccion, observacion)
            st.success('Cliente guardado exitosamente!')

    # Ejecutar la aplicación
    if __name__ == '__main__':
        main()
