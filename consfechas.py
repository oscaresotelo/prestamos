import streamlit as st
import sqlite3
import pandas as pd


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
local_css("estilos.css")

if "ingreso" not in st.session_state:
    st.session_state.ingreso = ""

if st.session_state.ingreso == "":
    st.warning("Por favor Ingrese Correctamente")
else:

    # Conexión a la base de datos
    conn = sqlite3.connect('financiera.db')
    cursor = conn.cursor()
    tab1 , tab2, tab3,tab4 = st.tabs(['Fecha Vto de Creditos','Fecha Vto y Cobrador', 'Fecha Otorgamiento', 'Otorgamiento Tipo Credito'])


    with tab1:
    # Función para ejecutar consultas SQL y obtener resultados en un DataFrame
        def run_query(query):
            cursor.execute(query)
            data = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            df = pd.DataFrame(data, columns=columns)
            return df

        # Obtener valores únicos para el campo TipoCredito
        tipos_credito_query = "SELECT DISTINCT TipoCredito FROM Credito"
        tipos_credito = run_query(tipos_credito_query)['TipoCredito'].tolist()

        # Crear formulario para seleccionar fechas y TipoCredito
        fecha_desde_tab1 = st.date_input('Seleccionar fecha desde:')
        fecha_hasta_tab1 = st.date_input('Seleccionar fecha hasta:')
        tipo_credito_seleccionado_tab1 = st.selectbox('Seleccionar TipoCredito:', tipos_credito)

        # Consulta SQL para obtener registros de la tabla DetalleCredito
        query = f"""
        SELECT Clientes.Nombre AS Cliente_Nombre, Clientes.Apellido AS Cliente_Apellido, 
               DetalleCredito.FechaVto, DetalleCredito.CuotaImporte, Cobradores.Nombre AS Cobrador_Nombre
        FROM DetalleCredito
        JOIN Credito ON DetalleCredito.IdCredito = Credito.IdCredito
        JOIN Clientes ON Credito.Dni = Clientes.Dni
        JOIN Cobradores ON Credito.IdCobrador = Cobradores.IdCobrador
        WHERE DetalleCredito.FechaVto BETWEEN '{fecha_desde_tab1}' AND '{fecha_hasta_tab1}'
              AND Credito.TipoCredito = '{tipo_credito_seleccionado_tab1}'
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

    with tab2:


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
        fecha_desde_tab2= st.date_input('Seleccionar fecha desde:', key='fecha_desde_tab2')
        fecha_hasta_tab2 = st.date_input('Seleccionar fecha hasta:', key='fecha_hasta_tab2')
        cobrador_seleccionado_nombre_tab2 = st.selectbox('Seleccionar Nombre de Cobrador:', cobradores_dict.keys())
        cobrador_seleccionado_id = cobradores_dict[cobrador_seleccionado_nombre_tab2]

        # Consulta SQL para obtener registros de la tabla DetalleCredito
        query = f"""
        SELECT Clientes.Nombre AS Cliente_Nombre, Clientes.Apellido AS Cliente_Apellido, 
               DetalleCredito.FechaVto, DetalleCredito.CuotaImporte, Cobradores.Nombre AS Cobrador_Nombre
        FROM DetalleCredito
        JOIN Credito ON DetalleCredito.IdCredito = Credito.IdCredito
        JOIN Clientes ON Credito.Dni = Clientes.Dni
        JOIN Cobradores ON Credito.IdCobrador = Cobradores.IdCobrador
        WHERE DetalleCredito.FechaVto BETWEEN '{fecha_desde_tab2}' AND '{fecha_hasta_tab2}'
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
    with tab3:
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
        fecha_desde_tab3 = st.date_input('Seleccionar fecha desde:',  key='fecha_desde_tab3')
        fecha_hasta_tab3 = st.date_input('Seleccionar fecha hasta:' ,  key='fecha_hasta_tab3')
        cobrador_seleccionado_nombre_tab3 = st.selectbox('Seleccionar Nombre de Cobrador:', cobradores_dict.keys(), key='seleccioncobrador')
        cobrador_seleccionado_id_tab3 = cobradores_dict[cobrador_seleccionado_nombre_tab3]

        # Consulta SQL para obtener registros de la tabla Credito
        query = f"""
        SELECT Clientes.Nombre AS Cliente_Nombre, Clientes.Apellido AS Cliente_Apellido, 
               Credito.FechaAlta, Credito.TipoCredito, Credito.Capital, Credito.SaldoCapital, Cobradores.Nombre AS Cobrador_Nombre
        FROM Credito
        JOIN Clientes ON Credito.Dni = Clientes.Dni
        JOIN Cobradores ON Credito.IdCobrador = Cobradores.IdCobrador
        WHERE Credito.FechaAlta BETWEEN '{fecha_desde_tab3}' AND '{fecha_hasta_tab3}'
              AND Cobradores.IdCobrador = {cobrador_seleccionado_id_tab3}
        """

        # Ejecutar la consulta y mostrar resultados en un DataFrame
        result_df = run_query(query)

        # Mostrar DataFrame en Streamlit
        st.dataframe(result_df)

        # Mostrar la cantidad de registros encontrados
        st.write(f"Cantidad de registros encontrados: {len(result_df)}")

        # Mostrar la suma del campo CuotaImporte
        total_con_interes = result_df["SaldoCapital"].sum()
        total_cuota_importe = result_df['Capital'].sum()
        st.write(f"Capital Prestado: {total_cuota_importe}")
        st.write(f'Total a Cobrar: {total_con_interes}')
        st.write(f'Ganancia: {total_con_interes - total_cuota_importe}')

    with tab4:
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
        fecha_desde_tab4 = st.date_input('Seleccionar fecha desde:', key='desdetab4')
        fecha_hasta_tab4 = st.date_input('Seleccionar fecha hasta:', key='hastatab4')

        # Consulta SQL para obtener registros de la tabla Credito
        query = f"""
        SELECT Clientes.Nombre AS Cliente_Nombre, Clientes.Apellido AS Cliente_Apellido, 
               Credito.FechaAlta, Credito.TipoCredito, Credito.Capital, Credito.SaldoCapital, Cobradores.Nombre AS Cobrador_Nombre
        FROM Credito
        JOIN Clientes ON Credito.Dni = Clientes.Dni
        JOIN Cobradores ON Credito.IdCobrador = Cobradores.IdCobrador
        WHERE Credito.FechaAlta BETWEEN '{fecha_desde_tab4}' AND '{fecha_hasta_tab4}'
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
