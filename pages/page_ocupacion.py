import streamlit as st

st.header("Modelo predictivo de ocupacion")

# ---------------------------------------------------------------------

# Diccionario de albergues por concello
albergues_por_concello = {
    "O Saviñao": ["Albergue Xacobeo Diamondi"],
    "Sarria": ["Alberue Xacobeo Barbadelo", "Albergue Xacobeo Calvor", "Albergue Xacobeo Sarria"],
    "Trasmiras": ["ALBERGUE VILADERREI"],
    "Castroverde": ["Albergue Xacobeo Castroverde"],
    "Muxía": ["Albergue Xacobeo Muxía"],
    "Sandiás": ["ALBERGUE SANDIÁS"],
    "Vilalba": ["Albergue Xacobeo Vilalba"],
    "Palas de Rei": ["Albergue Xacobeo Mato-Casanova", "Albergue Xacobeo Os Chacotes", "Albergue Xacobeo Palas de Rei"],
    "Mesía": ["Albergue Xacobeo Bruma"],
    "Pedrafita do Cebreiro": ["ALBERGUE XACOBEO HOSPITAL DA CONDESA", "Albergue Xacobeo O Cebreiro"],
    "Abadín": ["ALBERGUE XACOBEO Abadín"],
    "Vilar de Barrio": ["ALBERGUE VILAR DE BARRIO"],
    "Santiago de Compostela": ["Albergue Xacobeo San Lázaro", "Albergue Xacobeo Monte do Gozo"],
    "Ordes": ["Albergue Xacobeo Poulo"],
    "Guntín": ["Albergue Xacobeo Retorta"],
    "O Pino": ["Albergue Xacobeo Santa Irene"],
    "Vilasantar": ["Albergue Xacobeo Vilasantar"],
    "Vigo": ["Albergue Xacobeo Vigo"],
    "Arzúa": ["Albergue Xacobeo Ribadiso", "Albergue Xacobeo Arzúa"],
    "Redondela": ["Albergue Xacobeo Redonela"],
    "Xinzo de Limia": ["ALBERGUE XINZO DE LIMIA"],
    "Portomarín": ["Albergue Xacobeo Gonzar", "ALBERGUE XACOBEO Hospital da Cruz", "Albergue Xacobeo Portomarín"],
    "Tui": ["ALBERGUE TUI"],
    "Triacastela": ["Albergue Xacobeo Triacastela"],
    "Fonsagrada": ["Albergue Xacobeo Fonsagrada"],
    "Melide": ["Albergue Xacobeo Melide"],
    "Mondoñedo": ["Albergue Xacobeo Mondoñedo"],
    "Carral": ["Albergue Xacobeo Sergude"],
    "Miño": ["Albergue Xacobeo Miño"],
    "Verín": ["ALBERGUE VERIN"],
    "Vedra": ["ALBERGUE VEDRA"],
    "O Pino-Valga": ["ALBERGUE VALGA"],
    "Teo": ["Albergue Xacobeo TEO"],
    "Negreira": ["Albergue Xacobeo Negreira"],
    "Friol": ["Albergue Xacobeo A Cabana"],
    "Merlán": ["Albergue Xacobeo Seixas"],
    "Pontecesures": ["Albergue Xacobeo Pontecesures"],
    "Lusío": ["Albergue Xacobeo Casa Forte de Lusío"],
    "Boimorto": ["Albergue Xacobeo Boimorto"],
    "Porriño": ["ALBERGUE PORRINO"],
    "Lugo": ["Albergue Xacobeo Lugo"],
    "A Gudiña": ["Albergue Xacobeo A Gudiña"],
    "Ferrol": ["Albergue Público de Peregrinos de Ferrol"],
    "Monterroso": ["Albergue Xacobeo Ligonde"],
    "San Cristobo de Cea": ["MOSTEIRO DE OSEIRA"],
    "Lalín": ["ALBERGUE LALIN"],
    "Silleda": ["ALBERGUE BANDEIRA"],
    "Ourense": ["Albergue OURENSE"],
    "Ferreiros": ["Albergue Xacobeo Ferreiros"],
    "Ribadeo": ["Albergue Xacobeo Ribadeo"],
    "Betanzos": ["Albergue Xacobeo Betanzos"],
    "Begonte": ["Albergue Xacobeo Baamonde"],
    "O Pedrouzo (O Pino)": ["Albergue Xacobeo Arca"]
}

# Crear la lista de concellos a partir de las claves del diccionario
concellos = list(albergues_por_concello.keys())

# Primer desplegable para seleccionar el concello
tipo_opc = st.selectbox('Selecciona el concello:', concellos)

# Si se selecciona un concello, mostrar el desplegable con los albergues correspondientes
if tipo_opc in albergues_por_concello:
    albergues = albergues_por_concello[tipo_opc]
    albergue_selec = st.selectbox('Selecciona el albergue:', albergues)

