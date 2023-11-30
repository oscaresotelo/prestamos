
# import streamlit as st
# import sqlite3
# from datetime import datetime, timedelta
# import pandas as pd

# # Conectar a la base de datos SQLite
# conn = sqlite3.connect('financiera.db')
# cursor = conn.cursor()

# # Función para buscar y mostrar los datos de un cliente por DNI
# def mostrar_datos_cliente(dni):
#     cursor.execute('SELECT * FROM Clientes WHERE Dni = ?', (dni,))
#     cliente = cursor.fetchone()
#     if cliente:
#         st.write(f'**Nombre:** {cliente[3]} {cliente[4]}')
#         st.write(f'**Dirección:** {cliente[5]}')
#         st.write(f'**Observación:** {cliente[6]}')
#     else:
#         st.warning('Cliente no encontrado')

# def ingresar_credito(dni, tipo_credito, tipo_cobro, capital, cuotas, interes, importe_cuota, saldo_capital, activo, fecha_proximo_vto):
#     fecha_actual = datetime.now().strftime('%Y-%m-%d')  # Obtener la fecha actual en formato YYYY-MM-DD
#     cursor.execute('INSERT INTO Credito (Dni, TipoCredito, TipoCobro, Capital, CantidadCuotas, Interes, ImporteCuota, SaldoCapital, Activo, FeachaProximoiVto, FechaAlta, CantidadCuotasPagadas) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?,?)',
#                    (dni, tipo_credito, tipo_cobro.upper(), capital, cuotas, interes, importe_cuota, saldo_capital, activo, fecha_proximo_vto, fecha_actual, 0))
#     conn.commit()
#     st.success('Registro de crédito ingresado con éxito')

#     # Obtener el último IdCredito insertado
#     cursor.execute('SELECT last_insert_rowid()')
#     id_credito = cursor.fetchone()[0]

#     # Insertar registros en DetalleCredito
#     fecha_actual = datetime.now()
#     for numero_cuota in range(cuotas, 0, -1):
#         fecha_vto = fecha_actual + timedelta(days=30 * numero_cuota)  # Asumiendo pagos mensuales
#         cursor.execute('INSERT INTO DetalleCredito (IdCredito, FechaVto, CuotaImporte, Activo, NumeroCuota) VALUES (?, ?, ?, ?, ?)',
#                        (id_credito, fecha_vto.strftime('%Y-%m-%d'), importe_cuota, activo, numero_cuota))
    
#     conn.commit()

#     return id_credito  # Devolver el id_credito

# # Streamlit app
# st.title('Otorgamiento de Creditos')

# # Formulario para ingresar DNI y mostrar datos del cliente
# dni_cliente = st.text_input('Ingrese DNI del Cliente:')
# if st.button('Buscar Cliente'):
#     mostrar_datos_cliente(dni_cliente)

# # Formulario para ingresar registros en la tabla Creditos
# st.title('Ingresar Nuevo Crédito')
# tipo_credito_options = ["PERSONAL", "COMERCIAL"]
# tipo_credito = st.selectbox('Tipo de Crédito:', tipo_credito_options)
# tipo_cobro_options = ["MENSUAL", "SEMANAL"]
# tipo_cobro = st.selectbox('Tipo de Cobro:', tipo_cobro_options)
# capital = int(st.number_input('Capital:', min_value= 0))
# interes = st.number_input('Interés:', min_value = 40)
# nuevo_capital = capital + (capital * interes / 100)
# cuotas = int(st.number_input('Cantidad de Cuotas:', min_value= 0))
# importe_cuota = 0  # Inicializar importe_cuota con un valor predeterminado
# if cuotas != 0:
#     importe_cuota = nuevo_capital / cuotas
#     st.write(f'Importe de Cuotas: {importe_cuota}')
# total_pagar = nuevo_capital
# st.write(f'Importe Total del Crédito: {total_pagar}')
# activo = st.checkbox('Activo', value=True)
# fecha_proximo_vto = st.date_input('Fecha Próximo Vencimiento:')

# id_credito = None  # Inicializar id_credito

# if st.button('Ingresar Crédito'):
#     id_credito = ingresar_credito(dni_cliente, tipo_credito, tipo_cobro, capital, cuotas, interes, importe_cuota, total_pagar, activo, fecha_proximo_vto)

#     # Mostrar los datos de DetalleCredito en un DataFrame
#     if id_credito is not None:
#         cursor.execute('SELECT FechaVto, NumeroCuota, CuotaImporte FROM DetalleCredito WHERE IdCredito = ?  ORDER BY NumeroCuota ASC', (id_credito,))
#         detalle_credito_data = cursor.fetchall()
#         if detalle_credito_data:
#             df_detalle_credito = pd.DataFrame(detalle_credito_data, columns=['FechaVto', 'NumeroCuota', 'CuotaImporte'])
#             st.write(df_detalle_credito)
#         else:
#             st.warning('No hay datos en DetalleCredito para el crédito recién ingresado')

# # Cerrar la conexión a la base de datos al finalizar
# conn.close()
import streamlit as st
import sqlite3
from datetime import datetime, timedelta
import pandas as pd

# Conectar a la base de datos SQLite
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

    # Función para buscar y mostrar los datos de un cliente por DNI
    def mostrar_datos_cliente(dni):
        cursor.execute('SELECT * FROM Clientes WHERE Dni = ?', (dni,))
        cliente = cursor.fetchone()
        if cliente:
            st.write(f'**Nombre:** {cliente[3]} {cliente[4]}')
            st.write(f'**Dirección:** {cliente[5]}')
            st.write(f'**Observación:** {cliente[6]}')
        else:
            st.warning('Cliente no encontrado')

    def ingresar_credito(dni, tipo_credito, tipo_cobro, capital, cuotas, interes, importe_cuota, saldo_capital, activo, fecha_proximo_vto):
        fecha_actual = datetime.now().strftime('%Y-%m-%d')  # Obtener la fecha actual en formato YYYY-MM-DD
        cursor.execute('INSERT INTO Credito (Dni, TipoCredito, TipoCobro, Capital, CantidadCuotas, Interes, ImporteCuota, SaldoCapital, Activo, FeachaProximoiVto, FechaAlta, CantidadCuotasPagadas, IdCobrador) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?,?,?)',
                       (dni, tipo_credito, tipo_cobro.upper(), capital, cuotas, interes, importe_cuota, saldo_capital, activo, fecha_proximo_vto, fecha_actual, 0, st.session_state.idusuario))
        conn.commit()
        st.success('Registro de crédito ingresado con éxito')

        # Obtener el último IdCredito insertado
        cursor.execute('SELECT last_insert_rowid()')
        id_credito = cursor.fetchone()[0]

        # Insertar registros en DetalleCredito
        fecha_actual = datetime.now()
        dias_entre_cuotas = 7 if tipo_cobro.upper() == "SEMANAL" else 30  # Cambio a 7 días si el tipo de cobro es semanal
        for numero_cuota in range(cuotas, 0, -1):
            fecha_vto = fecha_actual + timedelta(days=dias_entre_cuotas * numero_cuota)
            cursor.execute('INSERT INTO DetalleCredito (IdCredito, FechaVto, CuotaImporte, Activo, NumeroCuota) VALUES (?, ?, ?, ?, ?)',
                           (id_credito, fecha_vto.strftime('%Y-%m-%d'), importe_cuota, activo, numero_cuota))
        
        conn.commit()

        return id_credito  # Devolver el id_credito

    # Streamlit app
    st.title('Otorgamiento de Créditos')

    # Formulario para ingresar DNI y mostrar datos del cliente
    dni_cliente = st.text_input('Ingrese DNI del Cliente:')
    if dni_cliente:
        mostrar_datos_cliente(dni_cliente)

    # Formulario para ingresar registros en la tabla Creditos
    st.title('Ingresar Nuevo Crédito')
    tipo_credito_options = ["PERSONAL", "COMERCIAL"]
    tipo_credito = st.selectbox('Tipo de Crédito:', tipo_credito_options)
    tipo_cobro_options = ["MENSUAL", "SEMANAL"]
    tipo_cobro = st.selectbox('Tipo de Cobro:', tipo_cobro_options)
    capital = int(st.number_input('Capital:', min_value=0))
    interes = st.number_input('Interés:', min_value=40)
    nuevo_capital = capital + (capital * interes / 100)
    cuotas = int(st.number_input('Cantidad de Cuotas:', min_value=0))
    importe_cuota = 0  # Inicializar importe_cuota con un valor predeterminado
    if cuotas != 0:
        importe_cuota = nuevo_capital / cuotas
        st.write(f'Importe de Cuotas: {importe_cuota}')
    total_pagar = nuevo_capital
    st.write(f'Importe Total del Crédito: {total_pagar}')
    activo = st.checkbox('Activo', value=True)
    fecha_proximo_vto = st.date_input('Fecha Próximo Vencimiento:')

    id_credito = None  # Inicializar id_credito

    if st.button('Ingresar Crédito'):
        id_credito = ingresar_credito(dni_cliente, tipo_credito, tipo_cobro, capital, cuotas, interes, importe_cuota, total_pagar, activo, fecha_proximo_vto)

        # Mostrar los datos de DetalleCredito en un DataFrame
        if id_credito is not None:
            cursor.execute('SELECT FechaVto, NumeroCuota, CuotaImporte FROM DetalleCredito WHERE IdCredito = ?  ORDER BY NumeroCuota ASC', (id_credito,))
            detalle_credito_data = cursor.fetchall()
            if detalle_credito_data:
                df_detalle_credito = pd.DataFrame(detalle_credito_data, columns=['FechaVto', 'NumeroCuota', 'CuotaImporte'])
                st.write(df_detalle_credito)
            else:
                st.warning('No hay datos en DetalleCredito para el crédito recién ingresado')

    # Cerrar la conexión a la base de datos al finalizar
    conn.close()
