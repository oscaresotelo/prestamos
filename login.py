import streamlit as st
import sqlite3
from st_pages import Page, show_pages, add_page_title
import base64

import pandas as pd

# Connect to the SQLite database
conn = sqlite3.connect("financiera.db")

# Create a cursor
c = conn.cursor()

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
                     .container {
                display: flex;
            }
            .logo-text {
                font-weight:700 !important;
                font-size:30px !important;
                color: black !important;
                padding-top: 50px !important;
            }
            .logo-img {
                float:right;
            }
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
st.title("Ingreso Sistema Principal")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

if "ingreso" not in st.session_state:
    st.session_state.ingreso = ""

if "usuario" not in st.session_state:
    st.session_state.usuario = ""
if "idusuario" not in st.session_state:
    st.session_state.idusuario = ""
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def login(user):
    st.session_state.ingreso = "ok"
    st.session_state.usuario = user[1]
    st.session_state.idusuario = user[0]
    st.write(st.session_state.usuario)
    if user[4] == 1:
        
        st.success("Bienvenido Administrador!")
        
        show_pages([
            Page("AltaClientes.py", "Alta De Clientes"),
            Page("AltaCreditos.py", "Alta De Creditos"),
            Page("AltaTipoCliente.py", "Alta Tipo Cliente"),
            Page("AltaTipoCredito.py", "Alta Tipo Credito"),
            Page("ConsultaCredito.py", "Consulta de Creditos"),
            Page("AltaUsuario.py", "Alta Modificacion Usuarios"),
            Page("prubalink.py", "Cobranza"),
            Page("consfechas.py", "Consulta General"),
            Page("registrodepagos.py", "Registrar Pagos"),
            Page("login.py", "Salir"),     
            ])
    elif user[4] == 2:
        st.success("Bienvenido Cobrador")
        
        show_pages([
            Page("AltaClientes.py", "Alta De Clientes"),
            Page("AltaCreditos.py", "Alta De Creditos"),
            
            Page("prubalink.py", "Cobranza"),
            Page("login.py", "Salir"), 
        ])

# Create the login form

if st.session_state.ingreso == "ok":
    st.title("Salir del Sistema")
    if st.button("salir"):
        del st.session_state.ingreso
        st.info("Salio Exitosamente del Sistema")
else:
    st.header("Ingrese")
    placeholder = st.empty()
    with placeholder.form("Login"):
        username = st.text_input("Usuario")
        password = st.text_input("Password", type="password")
        ingresar = st.form_submit_button("Ingresar")
    if ingresar:
        c.execute("SELECT * FROM Cobradores WHERE Dni = ? AND Pass = ?", (username, password))
        user = c.fetchone()
        if user is not None:
            login(user)
            placeholder.empty()
        else:
            st.error("Usuario o Contraseña Incorrecta")

# Add a submit button
local_css("estilos.css")

# Ejecutar la consulta SQL
