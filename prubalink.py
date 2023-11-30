
# import streamlit as st
# import sqlite3
# import pandas as pd
# from reportlab.pdfgen import canvas
# from io import BytesIO
# import base64
# from datetime import datetime
# import os
# import urllib.parse
# # Conexión a la base de datos SQLite
# conn = sqlite3.connect('financiera.db')
# cursor = conn.cursor()

# # Función para obtener la información de los créditos según la FechaVto
# def obtener_informacion_creditos_por_fecha(fecha_vto):
#     cursor.execute("""
#         SELECT Cl.Nombre, Cl.Apellido, Cl.Dni, DC.NumeroCuota, DC.CuotaImporte, DC.PagoImporte, DC.IdDetalle, Cl.Telefono
#         FROM DetalleCredito DC
#         JOIN Credito C ON DC.IdCredito = C.IdCredito
#         JOIN Clientes Cl ON C.Dni = Cl.Dni
#         WHERE DC.FechaVto = ?
#         """, (fecha_vto,))
#     resultados = cursor.fetchall()
#     return resultados

# # Función para actualizar el PagoImporte en la tabla DetalleCredito
# def actualizar_pago_importe(id_detalle, pago_importe):
#     iddetalle = int(id_detalle)
#     cursor.execute("""
#         UPDATE DetalleCredito
#         SET PagoImporte = ?
#         WHERE IdDetalle = ?
#         """, (pago_importe, iddetalle))
#     conn.commit()

# def generar_pdf(data, nombre_cliente, apellido_cliente):
#     buffer = BytesIO()
#     p = canvas.Canvas(buffer)

#     # Encabezado del PDF
#     p.setFont("Helvetica-Bold", 16)
#     p.drawCentredString(300, 800, "RECIBO DE PAGO")

#     # Contenido del PDF
#     p.setFont("Helvetica", 12)
#     y_position = 750
#     for row in data:
#         p.drawString(100, y_position, f"NOMBRE: {row[0]} {row[1]}")
#         p.drawString(100, y_position - 20, f"CUOTA : {row[3]}")
#         p.drawString(100, y_position - 40, f"CUOTA IMPORTE: {row[4]}")
#         p.drawString(100, y_position - 60, f"PAGO IMPORTE: {row[5]}")
#         p.drawString(100, y_position - 80, f"FECHA PAGO : {datetime.now().strftime('%Y-%m-%d')}")  # Reemplaza con la fecha actual
#         y_position -= 100
#     pdf_filename = f"{nombre_cliente}_{apellido_cliente}_recibo.pdf"
#     p.save()
#     buffer.seek(0)
#     st.write("PDF generado correctamente.")
#     return buffer, pdf_filename

# # Configuración de la aplicación Streamlit
# st.title('Consulta y Actualización de Créditos por Fecha de Vencimiento')

# # Verificación de la existencia de la Fecha de Vencimiento ingresada
# fecha_vto = st.date_input('Seleccione la Fecha de Vencimiento:')

# if 'copy_button_clicked' not in st.session_state:
#     st.session_state.copy_button_clicked = False

# # Verificación de la existencia de la Fecha de Vencimiento ingresada
# if fecha_vto:
#     # Obtener información de los créditos por Fecha de Vencimiento
#     info_creditos = obtener_informacion_creditos_por_fecha(str(fecha_vto))

#     # Mostrar la información en un DataFrame
#     if info_creditos:
#         df = pd.DataFrame(info_creditos, columns=['Clientes.Nombre', 'Clientes.Apellido', 'Clientes.dni', 'NumeroCuota', 'CuotaImporte', 'PagoImporte', 'IdDetalle', 'Clientes.Telefono'])
#         st.write(df)

#         # Formulario para ingresar el importe de pago y seleccionar el registro
#         selected_row = st.selectbox('Seleccione el registro para actualizar:', df.index, key='selectbox')
        
#         if selected_row is not None:
#             pago_importe = st.number_input('Ingrese el importe de pago:', min_value=0.0, step=1.0, key='number_input')

#             if st.button('Actualizar PagoImporte'):
#                 id_detalle = df.iloc[selected_row]['IdDetalle']
#                 actualizar_pago_importe(id_detalle, pago_importe)
#                 st.success('PagoImporte actualizado correctamente.')

#                 info_creditos_actualizado = obtener_informacion_creditos_por_fecha(str(fecha_vto))
                
#                 # Obtener el nombre y apellido del cliente seleccionado
#                 nombre_cliente = df.iloc[selected_row]['Clientes.Nombre']
#                 apellido_cliente = df.iloc[selected_row]['Clientes.Apellido']

#                 # Generar el PDF con el nombre del cliente
#                 pdf_data, pdf_filename = generar_pdf([info_creditos_actualizado[selected_row]], nombre_cliente, apellido_cliente)
#                 pdf_download_link = f'data:application/pdf;base64,{base64.b64encode(pdf_data.getvalue()).decode("utf-8")}'
#                 telefono = df.iloc[selected_row]['Clientes.Telefono']
#                 # whatsapp_message = f"Hola {nombre_cliente} {apellido_cliente}, tu recibo de pago está disponible. Descárgalo aquí: {pdf_download_link}"
#                 whatsapp_message = f"{pdf_download_link}"
#                 whatsapp_url = f"https://wa.me/{telefono}?text={urllib.parse.quote(whatsapp_message)}"

#                 # whatsapp_url = f"https://wa.me/{telefono}"
#                 # # Guardar el PDF en la carpeta raíz
#                 pdf_path = os.path.join(os.getcwd(), pdf_filename)
#                 with open(pdf_path, 'wb') as pdf_file:
#                     pdf_file.write(pdf_data.getvalue())

#                 # Mostrar el enlace de descarga del PDF con el nombre del cliente
#                 pdf_download_link = f'data:application/pdf;base64,{base64.b64encode(pdf_data.getvalue()).decode("utf-8")}'
#                 st.markdown(f'Descarga el PDF aquí: [Descargar PDF]({pdf_download_link})')

#                 # Mostrar el enlace de WhatsApp
#                 st.write("Enviar Mensaje")
#                 st.markdown(f"[![Icono de WhatsApp](https://img.icons8.com/color/48/000000/whatsapp--v1.png)]({whatsapp_url})")

#                 # Copiar el enlace al portapapeles
#                 # if st.button('Copiar enlace al portapapeles') or st.session_state.copy_button_clicked:
#                 #     st.session_state.copy_button_clicked = True
#                 #     st.clipboard.write_text(pdf_download_link)
#                 #     st.success('Enlace copiado al portapapeles')

#     else:
#         st.warning('No hay créditos para la Fecha de Vencimiento seleccionada.')

# # Cerrar la conexión a la base de datos al finalizar
# conn.close()
import streamlit as st
import sqlite3
import pandas as pd
from reportlab.pdfgen import canvas
from io import BytesIO
import base64
from datetime import datetime
import os
import urllib.parse

if "ingreso" not in st.session_state:
    st.session_state.ingreso = ""

st.markdown(f"<h1 style='text-align: center; color: black;'> Usuario: {st.session_state.usuario}</h1>", unsafe_allow_html=True)

if "usuario" not in st.session_state:
    st.session_state.idusuario = ""
if st.session_state.ingreso == "":
    st.warning("Por favor Ingrese Correctamente")
else:
    def local_css(file_name):
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    local_css("estilos.css")

    # Conexión a la base de datos SQLite
    conn = sqlite3.connect('financiera.db')
    cursor = conn.cursor()

    # Función para obtener la información de los créditos según la FechaVto
    def obtener_informacion_creditos_por_fecha(fecha_vto):
        cursor.execute("""
            SELECT Cl.Nombre, Cl.Apellido, Cl.Dni, Cl.Direccion, DC.NumeroCuota, DC.CuotaImporte, DC.PagoImporte, DC.IdDetalle, Cl.Telefono
            FROM DetalleCredito DC
            JOIN Credito C ON DC.IdCredito = C.IdCredito
            JOIN Clientes Cl ON C.Dni = Cl.Dni
            WHERE DC.FechaVto = ?
            """, (fecha_vto,))
        resultados = cursor.fetchall()
        return resultados

    # Función para actualizar el PagoImporte en la tabla DetalleCredito y actualizar la información en la tabla Creditos
    def actualizar_pago_importe(id_detalle, pago_importe):
        fecha_actual = datetime.now().strftime('%Y-%m-%d')
        iddetalle = int(id_detalle)
        
        # Obtener la información necesaria de DetalleCredito para actualizar Creditos
        cursor.execute("""
            SELECT DC.IdCredito, DC.NumeroCuota
            FROM DetalleCredito DC
            WHERE DC.IdDetalle = ?
            """, (iddetalle,))
        credito_info = cursor.fetchone()
        
        id_credito = credito_info[0]
        numero_cuota = credito_info[1]
        NumeroCobrador = st.session_state.idusuario
        # Actualizar el PagoImporte en DetalleCredito
        cursor.execute("""
            UPDATE DetalleCredito
            SET PagoImporte = ?, IdCobrador = ? , FechaPago = ?
            WHERE IdDetalle = ?
            """, (pago_importe, NumeroCobrador,fecha_actual,iddetalle))
        
        # Actualizar la información en la tabla Creditos
        cursor.execute("""
            UPDATE Credito
            SET CantidadCuotasPagadas = CantidadCuotasPagadas + 1,
                FechaUltimoPago = ?
            WHERE IdCredito = ?
            """, (datetime.now().strftime('%Y-%m-%d'), id_credito))
        
        conn.commit()

    def generar_pdf(data, nombre_cliente, apellido_cliente):
        buffer = BytesIO()
        p = canvas.Canvas(buffer)

        # Encabezado del PDF
        p.setFont("Helvetica-Bold", 16)
        p.drawCentredString(300, 800, "RECIBO DE PAGO")

        # Contenido del PDF
        p.setFont("Helvetica", 12)
        y_position = 750
        for row in data:
            p.drawString(100, y_position, f"NOMBRE: {row[0]} {row[1]}")
            p.drawString(100, y_position - 20, f"CUOTA : {row[3]}")
            p.drawString(100, y_position - 40, f"CUOTA IMPORTE: {row[4]}")
            p.drawString(100, y_position - 60, f"PAGO IMPORTE: {row[5]}")
            p.drawString(100, y_position - 80, f"FECHA PAGO : {datetime.now().strftime('%Y-%m-%d')}")  # Reemplaza con la fecha actual
            y_position -= 100
        pdf_filename = f"{nombre_cliente}_{apellido_cliente}_recibo.pdf"
        p.save()
        buffer.seek(0)
        st.write("PDF generado correctamente.")
        return buffer, pdf_filename

    # Configuración de la aplicación Streamlit
    st.title('Registro de Pagos')

    # Verificación de la existencia de la Fecha de Vencimiento ingresada
    fecha_vto = st.date_input('Seleccione la Fecha de Vencimiento:')

    if 'copy_button_clicked' not in st.session_state:
        st.session_state.copy_button_clicked = False

    # Verificación de la existencia de la Fecha de Vencimiento ingresada
    if fecha_vto:
        # Obtener información de los créditos por Fecha de Vencimiento
        info_creditos = obtener_informacion_creditos_por_fecha(str(fecha_vto))

        # Mostrar la información en un DataFrame
        if info_creditos:
            df = pd.DataFrame(info_creditos, columns=['Clientes.Nombre', 'Clientes.Apellido', 'Clientes.dni', 'Clientes.Direccion','NumeroCuota', 'CuotaImporte', 'PagoImporte', 'IdDetalle', 'Clientes.Telefono'])
            st.write(df)

            # Formulario para ingresar el importe de pago y seleccionar el registro
            selected_row = st.selectbox('Seleccione el Credito:', df.index, key='selectbox')
            
            if selected_row is not None:
                pago_importe = st.number_input('Ingrese el importe de pago:', min_value=0.0, step=1.0, key='number_input')

                if st.button('Cargar Pago'):
                    id_detalle = df.iloc[selected_row]['IdDetalle']
                    actualizar_pago_importe(id_detalle, pago_importe)
                    st.success('Pago Cargado correctamente.')

                    info_creditos_actualizado = obtener_informacion_creditos_por_fecha(str(fecha_vto))
                    
                    # Obtener el nombre y apellido del cliente seleccionado
                    nombre_cliente = df.iloc[selected_row]['Clientes.Nombre']
                    apellido_cliente = df.iloc[selected_row]['Clientes.Apellido']

                    # Generar el PDF con el nombre del cliente
                    pdf_data, pdf_filename = generar_pdf([info_creditos_actualizado[selected_row]], nombre_cliente, apellido_cliente)
                    pdf_download_link = f'data:application/pdf;base64,{base64.b64encode(pdf_data.getvalue()).decode("utf-8")}'
                    telefono = df.iloc[selected_row]['Clientes.Telefono']
                    whatsapp_message = f"{pdf_download_link}"
                    whatsapp_url = f"https://wa.me/{telefono}?text={urllib.parse.quote(whatsapp_message)}"

                    # Guardar el PDF en la carpeta raíz
                    pdf_path = os.path.join(os.getcwd(), pdf_filename)
                    with open(pdf_path, 'wb') as pdf_file:
                        pdf_file.write(pdf_data.getvalue())

                    # Mostrar el enlace de descarga del PDF con el nombre del cliente
                    pdf_download_link = f'data:application/pdf;base64,{base64.b64encode(pdf_data.getvalue()).decode("utf-8")}'
                    st.markdown(f'Descarga el PDF aquí: [Descargar PDF]({pdf_download_link})')

                    # Mostrar el enlace de WhatsApp
                    st.write("Enviar Mensaje")
                    st.markdown(f"[![Icono de WhatsApp](https://img.icons8.com/color/48/000000/whatsapp--v1.png)]({whatsapp_url})")

    # Cerrar la conexión a la base de datos al finalizar
    conn.close()
