import streamlit as st
import sqlite3


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

    # Función para obtener la información de todos los créditos según el DNI
    def obtener_informacion_creditos(dni):
        cursor.execute("""
            SELECT C.TipoCredito, C.TipoCobro, C.FechaAlta, C.Capital, C.Interes,
                   C.CantidadCuotas, C.ImporteCuota, C.SaldoCapital, C.CantidadCuotasPagadas
            FROM Credito C
            JOIN Clientes Cl ON C.Dni = Cl.Dni
            WHERE C.Dni = ?
            """, (dni,))
        resultados = cursor.fetchall()
        return resultados

    # Configuración de la aplicación Streamlit
    st.title('Consulta de Créditos por DNI')

    # Formulario para ingresar el DNI
    dni = st.text_input('Ingrese el DNI del cliente:')

    # Verificación de la existencia del DNI ingresado
    if dni:
        # Obtener información de todos los créditos
        info_creditos = obtener_informacion_creditos(int(dni))

        # Mostrar la información en la aplicación
        if info_creditos:
            st.header('Información de Créditos')
            for credito in info_creditos:
                st.write(f'Tipo de Crédito: {credito[0]}')
                st.write(f'Tipo de Cobro: {credito[1]}')
                st.write(f'Fecha de Alta: {credito[2]}')
                st.write(f'Capital: {credito[3]}')
                st.write(f'Interés: {credito[4]}')
                st.write(f'Cantidad de Cuotas: {credito[5]}')
                st.write(f'Importe de Cuota: {credito[6]}')
                st.write(f'Total a Pagar: {credito[7]}')
                st.write(f'Cuotas Pagadas: {credito[8]}')
                st.write(f'Total Pagado: {credito[8] * credito[6]}')
              
                
                st.markdown(f"<h1 style='text-align: center; color: red;'> DEUDA RESTANTE: {credito[7] - credito[8] * credito[6]}</h1>", unsafe_allow_html=True)

                st.header(f'', divider="red")
                st.markdown('---')  # Separador entre registros
        else:
            st.warning('El DNI ingresado no existe en la base de datos.')

    # Cerrar la conexión a la base de datos al finalizar
    conn.close()
