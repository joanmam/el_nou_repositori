def generar_html_fontawesome2(ID_Recepte, titol, data_formatejada, imatge_url, ingredients, temps_preparacio, temps_act):
    return f"""
    <div style="margin-bottom: 10px;">
        <div style="display: grid; grid-template-columns: 1fr; grid-template-rows: auto auto auto auto; gap: 10px; border: 1px solid #ff3333; border-radius: 10px; padding: 0px; background-color: #ffd1b3;">
            <!-- Primera fila: Imatge y detalles -->
            <div style="display: flex; align-items: flex-start; grid-column: 1 / span 1;">
                <img src="{imatge_url}" alt="Imatge de la recepta" style="width: 150px; height: auto; border-radius: 8px; margin-bottom: 16px;">
                <div style="text-align: left; padding-left: 10px;">
                    <div style="display: flex; flex-direction: row; align-items: center; gap: 5px;"> <!-- Reducir el gap aquí -->
                        <h6 style="color: #000099; margin: 0;">{ID_Recepte}</h6>
                        <h4 style="margin: 0; padding-bottom: 0;">{titol}</h4>
                    </div>
                    <h6 style="color: #ff0000; margin: 0; display: block;">{data_formatejada}</h6>
                </div>
            </div>
            <!-- Segona fila: Temps de Preparació i Temps Total -->
            <div style="grid-column: 1 / span 1; display: flex; justify-content: flex-start; gap: 20px; align-items: center; padding-left: 10px;">
                <p style="display: flex; align-items: center; gap: 5px;">
                    <i class="fas fa-clock" style="font-size: 18px; vertical-align: middle;"></i>
                    {temps_preparacio} min
                </p>
                <p style="display: flex; align-items: center; gap: 5px;">
                    <i class="fas fa-hourglass" style="font-size: 18px; vertical-align: middle;"></i>
                    {temps_act} min
                </p>
            </div>
            <!-- Ingredients -->
            <div style="display: flex; align-items: center; gap: 5px; padding-left: 10px;">
                <i class="fas fa-shopping-cart" style="font-size: 18px; vertical-align: middle;"></i>
                {ingredients}
            </div>
        </div>
    </div>
    """