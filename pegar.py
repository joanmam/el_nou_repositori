import pandas as pd
import streamlit as st

# Exemple de dataframe
df_apats = pd.DataFrame({
    "Recepte": ["Paella", "Fideuà", "Truita"],
    "Imatge URL 1": ["img1.jpg", "img2.jpg", "img3.jpg"],
    "URL 1": ["https://example.com/1", "https://example.com/2", "https://example.com/3"],
    "Imatge URL 2": ["img4.jpg", "img5.jpg", "img6.jpg"],
    "URL 2": ["https://example.com/4", "https://example.com/5", "https://example.com/6"]
})

# Aplicar estils correctament
df_styled = df_apats.style.set_table_styles([
    {"selector": "th", "props": [("text-align", "center"), ("font-weight", "bold")]},
    {"selector": "td", "props": [("padding", "10px")]}
], overwrite=False)

# Mostrar el dataframe amb Streamlit
st.dataframe(df_styled, hide_index=True, use_container_width=True)