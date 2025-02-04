import streamlit as st
import streamlit.components.v1 as components

# Títol de l'aplicació
st.title('Entrada de data amb format DD-MM-YY')

# HTML i JavaScript per al selector de dates flatpickr
date_picker_html = """
<html>
<head>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/flatpickr/4.6.9/flatpickr.min.css">
</head>
<body>
    <input type="text" id="datepicker" style="width: 100%; padding: 10px; font-size: 16px;"/>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/flatpickr/4.6.9/flatpickr.min.js"></script>
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            flatpickr("#datepicker", {
                dateFormat: "d-m-Y",
                locale: {
                    firstDayOfWeek: 1,
                    weekdays: {
                        shorthand: ['Dg', 'Dl', 'Dt', 'Dc', 'Dj', 'Dv', 'Ds'],
                        longhand: [
                            'Diumenge', 'Dilluns', 'Dimarts', 'Dimecres',
                            'Dijous', 'Divendres', 'Dissabte'
                        ]
                    },
                    months: {
                        shorthand: ['Gen', 'Feb', 'Març', 'Abr', 'Maig', 'Jun', 'Jul', 'Ag', 'Set', 'Oct', 'Nov', 'Des'],
                        longhand: [
                            'Gener', 'Febrer', 'Març', 'Abril', 'Maig', 'Juny',
                            'Juliol', 'Agost', 'Setembre', 'Octubre', 'Novembre', 'Desembre'
                        ]
                    }
                },
                onChange: function(selectedDates, dateStr, instance) {
                    document.dispatchEvent(new CustomEvent('dateSelected', {detail: dateStr}));
                }
            });
        });
    </script>
</body>
</html>
"""

# Inserir el selector de dates a Streamlit
selected_date = components.html(date_picker_html, height=300)

# Recuperar la data seleccionada utilitzant JavaScript
date_placeholder = st.empty()
date_placeholder.text('Selecciona una data en el calendari.')

# Capturar l'esdeveniment de selecció de data
st.session_state.selected_date = None

date_js = """
<script>
document.addEventListener('dateSelected', function(e) {
    const selectedDate = e.detail;
    document.querySelector("#date-output").innerText = 'Data seleccionada: ' + selectedDate;
    streamlit.setComponentValue(selectedDate);
});
</script>
"""
components.html(date_js, height=0)

# Mostrar la data seleccionada
date_output = st.empty()
if st.session_state.selected_date:
    date_output.text('Data seleccionada: ' + st.session_state.selected_date)
else:
    date_output.text('Selecciona una data en el calendari.')
