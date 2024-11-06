import streamlit as st
from utils import general as gen

st.set_page_config(page_title="Modelo predictivo de flujos")

col1, col2, col3 = st.columns([3,3,3])
with col1:
    st.image("amtega_logo.png_2089811488.png", use_column_width=True)
with col3:
    st.header("SMETRIA")

st.divider()

st.header("Modelo predictivo de flujos")
# ---------------------------------------------------------------------------------
gen.login()