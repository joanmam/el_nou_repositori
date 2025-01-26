import streamlit as st
import sqlite3

# Connectar-se a la base de dades amb les claus estrangeres habilitades
conn = sqlite3.connect('C:/Users/Joan/Receptes/LesReceptes2/nova_base_de_dades.db')
conn.execute("PRAGMA foreign_keys = ON")  # Assegurar que les claus estrangeres estan habilitades
cursor = conn.cursor()

# Obtenir l'ID del registre a esborrar amb valor mínim de 1
record_id = int(st.number_input("ID del registre a borrar", min_value=1, step=1))

st.write(f"El registre seleccionat és el {record_id}")
st.write("Aquesta és la Recepta")

# Executar l'ordre SELECT amb el paràmetre
cursor.execute('SELECT * FROM Receptes WHERE ID_Recepte = ?', (record_id,))
record = cursor.fetchone()

# Mostrar el registre seleccionat
if record:
    st.write(f"ID: {record[0]}, Títol: {record[2]}, Data_formatejada: {record[1]}")
else:
    st.write("No s'ha trobat cap registre amb aquest ID.")

# Esborrar el registre seleccionat si existeix
if st.button("Esborrar"):
    if record:  # Comprovar que el registre existeix abans d'esborrar
        cursor.execute('DELETE FROM Receptes WHERE ID_Recepte = ?', (record_id,))
        conn.commit()
        st.success("Registre esborrat amb èxit!")

        # Comprovar si els registres relacionats s'han esborrat de la taula ingredients
        cursor.execute('SELECT * FROM ingredients WHERE ID_Recepte = ?', (record_id,))
        remaining_records = cursor.fetchall()
        if not remaining_records:
            st.write("Els registres relacionats s'han esborrat correctament.")
        else:
            st.write("Els registres relacionats NO s'han esborrat.")
    else:
        st.error("No s'ha trobat cap registre amb aquest ID. No es pot esborrar.")

# Tancar la connexió
conn.close()
