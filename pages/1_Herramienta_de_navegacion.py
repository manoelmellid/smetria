import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Herramienta de navegacion",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

col1, col2, col3 = st.columns([3,3,3])
with col1:
    st.image("amtega_logo.png_2089811488.png", use_column_width=True)
with col3:
    st.header("SMETRIA")

st.divider()

st.header("Herramienta de navegacion geospacial")
# Aquí incluirías todo el código específico para la predicción
