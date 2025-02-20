from altres.imports import *

st.set_page_config(layout="wide")



# Conectarse a la base de datos
conn = sqlitecloud.connect(cami_db)
cursor = conn.cursor()

conn.commit()
#_______________________________________________________________
rellotge()
st.header("Esborrar")
base64_image, cropped_image = cropping()
banner(base64_image)
#_________________________________________________________________________________________
# Conectarse a la base de datos
conn = sqlitecloud.connect(cami_db)
conn.execute("PRAGMA foreign_keys = ON")
cursor = conn.cursor()

#__________________________________________________________

# Obtenir els IDs dels registres a esborrar
st.write("")
st.write("")
lletra_variable()
st.markdown('<div class="custom-element"><p class="custom-title">Registres a esborrar separats per commes:</p>', unsafe_allow_html=True)
ids_to_delete = st.text_input("", "1,2,3")
ids_to_delete = [int(x) for x in ids_to_delete.split(",")]

st.write(f"Els registres seleccionats per esborrar són: {ids_to_delete}")

# Crear la cadena de placeholders per a la consulta
placeholders = ', '.join(['?' for _ in ids_to_delete])

# Mostrar informació dels registres seleccionats
query = f'SELECT ID_Recepte, Titol FROM Receptes WHERE ID_Recepte IN ({placeholders})'
cursor.execute(query, ids_to_delete)
records_to_show = cursor.fetchall()



for record in records_to_show:
    data = {
        'ID_Recepte': record[0],
        'Titol': record[1],
    }
    card_html = crear_tarjeta_html_resumida(data)
    st.markdown(card_html, unsafe_allow_html=True)


# Esborrar el registre seleccionat si existeix
if st.button("Esborrar"):
    for record_id in ids_to_delete:
        cursor.execute('DELETE FROM Receptes WHERE ID_Recepte = ?', (record_id,))
    conn.commit()


    # Comprovar si els registres relacionats s'han esborrat de la taula ingredients
    cursor.execute('SELECT * FROM ingredients WHERE ID_Recepte IN ({})'.format(','.join(['?'] * len(ids_to_delete))),
                   ids_to_delete)
    remaining_records = cursor.fetchall()
    if not remaining_records:
        st.success("Els registres relacionats s'han esborrat correctament.")
    else:
        st.error("Els registres relacionats NO s'han esborrat.")

# Tancar la connexió
conn.close()
