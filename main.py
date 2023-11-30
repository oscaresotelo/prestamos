import streamlit as st
import sqlite3
import datetime

# Conexión a la base de datos SQLite
conn = sqlite3.connect('credit_system.db')
cursor = conn.cursor()

# Crear tablas si no existen
cursor.execute('''
    CREATE TABLE IF NOT EXISTS loans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_name TEXT,
        amount REAL,
        installments INTEGER,
        interest_rate REAL,
        insurance_amount REAL,
        payment_frequency TEXT,
        total_payment REAL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS payments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        loan_id INTEGER,
        payment_date DATE,
        amount_paid REAL,
        FOREIGN KEY (loan_id) REFERENCES loans (id)
    )
''')
conn.commit()

# Función para calcular el total del préstamo
def calculate_payment(amount, installments, interest_rate, insurance_amount, payment_frequency):
    interest_rate /= 100.0
    if payment_frequency == "Diario":
        total_payment = amount * (1 + interest_rate) / installments + insurance_amount
    elif payment_frequency == "Semanal":
        total_payment = amount * (1 + interest_rate) / (installments // 4) + insurance_amount
    elif payment_frequency == "Quincenal":
        total_payment = amount * (1 + interest_rate) / (installments // 2) + insurance_amount
    elif payment_frequency == "Mensual":
        total_payment = amount * (1 + interest_rate) / installments + insurance_amount
    else:
        total_payment = amount * (1 + interest_rate) + insurance_amount

    return round(total_payment, 2)

# Interfaz de la aplicación con Streamlit
def main():
    st.title("Sistema de Créditos")

    # Formulario para ingresar los datos del préstamo
    client_name = st.text_input("Nombre del Cliente:")
    amount = st.number_input("Monto del Préstamo:")
    installments = st.number_input("Número de Cuotas:", min_value=1, step=1)
    interest_rate = st.number_input("Tasa de Interés (%):", min_value=0.0, step=0.1)
    insurance_amount = st.number_input("Monto del Seguro:")
    payment_frequency = st.selectbox("Frecuencia de Pago:", ["Diario", "Semanal", "Quincenal", "Mensual", "Anual"])

    if st.button("Calcular"):
        total_payment = calculate_payment(amount, installments, interest_rate, insurance_amount, payment_frequency)

        # Mostrar el plan de pago
        st.write("Plan de Pago:")
        st.write(f"Total a Pagar: {total_payment}")

        # Guardar en la base de datos
        cursor.execute('''
            INSERT INTO loans (client_name, amount, installments, interest_rate, insurance_amount, payment_frequency, total_payment)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (client_name, amount, installments, interest_rate, insurance_amount, payment_frequency, total_payment))
        conn.commit()

    # Realizar un pago
    st.header("Registro de Pagos")
    loan_id = st.selectbox("Seleccionar Préstamo:", cursor.execute("SELECT id, client_name FROM loans").fetchall())
    amount_paid = st.number_input("Monto Pagado:")
    payment_date = st.date_input("Fecha de Pago:", datetime.date.today())

    if st.button("Registrar Pago"):
        cursor.execute('''
            INSERT INTO payments (loan_id, payment_date, amount_paid)
            VALUES (?, ?, ?)
        ''', (loan_id, payment_date, amount_paid))
        conn.commit()
        st.success("Pago registrado exitosamente.")

if __name__ == '__main__':
    main()
