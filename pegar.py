# HTML complet amb tots els elements dins d'un únic contenidor
st.markdown("""
    <div style="border: 1px solid red; border-radius: 10px; padding: 20px; background-color: #f9f9f9;">

        <!-- Primer multiselect -->
        <div style="margin-bottom: 20px;">
            <p style="font-size: 16px; color: #333; margin-bottom: 5px; font-weight: bold;">Selecciona la primera categoria:</p>
        </div>

        <!-- Espai reservat per al primer multiselect -->
        <div id="multiselect-1"></div>

        <!-- Segon multiselect -->
        <div style="margin-bottom: 20px;">
            <p style="font-size: 16px; color: #333; margin-bottom: 5px; font-weight: bold;">Selecciona la segona categoria:</p>
        </div>

        <!-- Espai reservat per al segon multiselect -->
        <div id="multiselect-2"></div>

        <!-- Slider -->
        <div style="margin-bottom: 20px;">
            <p style="font-size: 16px; color: #333; margin-bottom: 5px; font-weight: bold;">Selecciona un valor:</p>
        </div>

        <!-- Espai reservat per al slider -->
        <div id="slider"></div>

    </div>
""", unsafe_allow_html=True)

# Afegir el primer multiselect
categoria1 = st.multiselect('', ['Tots', 'Cat1', 'Cat2', 'Cat3'], default=['Tots'])

# Afegir el segon multiselect
categoria2 = st.multiselect('', ['Opció1', 'Opció2', 'Opció3', 'Opció4'], default=[])

# Afegir el slider
temps_prep = st.slider('', 0, 240, (0, 240), step=1)
