import streamlit as st

st.title("About Me")

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("fahmi.png", width=120)

st.write(
    """
    Nama   : FAHMI RIDANI   

    NIM     : 2210031802152  
    
    Program Studi : TEKNIK INFORMATIKA 

    Universitas : Universitas Sains dan Teknologi Indonesia
    """
)
