import streamlit as st

# CSS per canviar la mida de la lletra del títol, ajustar el marge inferior i afegir un fons gris
st.markdown(
    """
    <style>
    .custom-title {
        font-size: 24px; /* Ajusta aquesta mida segons les teves necessitats */
        font-weight: bold;
        margin-bottom: 0.2em; /* Utilitza una unitat més petita per ajustar la separació */
    }
    .custom-element {
        background-color: #f0f0f0; /* Tono gris clar */
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 20px; /* Ajusta el marge inferior */
    }
    .separator {
        width: 100%;
        height: 2px;
        background-color: #123456; /* Pots canviar el color segons les teves necessitats */
        margin: 20px 0; /* Ajusta el marge segons les teves necessitats */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Utilitza HTML per aplicar la classe CSS al títol del primer multiselect i el fons gris
st.markdown('<div class="custom-element"><p class="custom-title">Selecciona una categoria:</p>', unsafe_allow_html=True)

# El teu primer st.multiselect aquí
categoria1 = st.multiselect('', ['Tots', 'Cat1', 'Cat2', 'Cat3'], default=['Tots'])

st.markdown('</div>', unsafe_allow_html=True)

# Afegir separador després del primer st.multiselect
st.markdown('<div class="separator"></div>', unsafe_allow_html=True)

# Utilitza HTML per aplicar la classe CSS al títol del segon slider i el fons gris
st.markdown('<div class="custom-element"><p class="custom-title">Selecciona un valor:</p>', unsafe_allow_html=True)

# El teu st.slider aquí
valor = st.slider('', min_value=0, max_value=100, value=50)

st.markdown('</div>', unsafe_allow_html=True)

# Afegir separador després del st.slider
st.markdown('<div class="separator"></div>', unsafe_allow_html=True)

# Un altre multiselect d'exemple amb fons gris
st.markdown('<div class="custom-element"><p class="custom-title">Selecciona un altre element:</p>', unsafe_allow_html=True)
categoria2 = st.multiselect('', ['Element 1', 'Element 2', 'Element 3'], default=['Element 1'])

st.markdown('</div>', unsafe_allow_html=True)

# Afegir separador després del segon st.multiselect
st.markdown('<div class="separator"></div>', unsafe_allow_html=True)

st.write(f"Has seleccionat de la primera categoria: {categoria1}")
st.write(f"Has seleccionat el valor: {valor}")
st.write(f"Has seleccionat de la segona categoria: {categoria2}")
