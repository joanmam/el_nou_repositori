from altres.imports import *



st.set_page_config(layout="wide")


rellotge()
#___________________________________________________________________________________
st.header('Protocol')
#______________________________________________________________________________________
base64_image, cropped_image = cropping()
banner(base64_image)


# Establir la connexió amb SQLite Cloud
conn = sqlitecloud.connect(cami_db)



receptes_seleccionades = st.text_input("Selecciona els ID de les receptes:")

if st.button("Seleccionar"):
    query = "SELECT ID_Recepte, Titol FROM Receptes WHERE ID_Recepte = ?"
    df = pd.read_sql(query, conn, params=[receptes_seleccionades])





# pels passos
    query2 = "SELECT Numero, Imatge_passos, Pas FROM Passos WHERE ID_Recepte = ?"
    df = pd.read_sql(query2, conn, params=[receptes_seleccionades])
    # Converteix cada blob a una imatge i crea una nova columna amb les imatges
    df['Miniatura'] = df['Imatge_passos'].apply(create_thumbnail2)

    # Oculta la columna del blob
    df = df[['Numero', 'Miniatura', 'Pas']]

    # Aplica l'estil de les files i les columnes
    styled_df = df.style.apply(row_style, axis=1)



    # Genera l'HTML estilitzat
    html = styled_df.hide(axis='index').to_html()
    html = html.replace('<style type="text/css">', '<style type="text/css">.row0 {background-color: #f0f0f0;} .row1 {background-color: #ffffff;}')

    # Crida la funció per mostrar el dataframe passant l'HTML com a paràmetre
    taula = dataframe_passos(html)

    # Mostra el DataFrame estilitzat utilitzant Streamlit
    st.components.v1.html(taula, height=600, scrolling=True)
