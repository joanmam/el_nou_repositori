import streamlit as st

# Definició del CSS per al marc i el text
css = """
<style>
.marco {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 300px;
    height: 150px;
    border: 5px solid #000000;  /* Borde de color negre */
    border-radius: 15px;  /* Bordes arrodonits */
    font-size: 24px;  /* Mida de la font */
    font-weight: bold;
    color: #000000;  /* Color del text */
    background-color: #FFFFFF;  /* Fons blanc */
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);  /* Una mica d'ombra per a millorar la visibilitat */
    text-align: center;  /* Text centrat */
    padding: 10px;  /* Espai intern al voltant del contingut */
}
</style>
"""

# Aplica el CSS utilitzant st.markdown
st.markdown(css, unsafe_allow_html=True)

# Contingut de l'aplicació
st.title("Benvingut a la meva pàgina")
st.write("Això és un paràgraf d'exemple.")

# Afegir text dins d'un marc amb l'estil definit
st.markdown('<div class="marco">Les Receptes de la Mamen</div>', unsafe_allow_html=True)


