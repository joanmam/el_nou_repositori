<div style="background-color:#ffffff; padding:10px; border-radius:5px; margin:10px; border:1px solid #ccc;">
    <!-- Taula amb tres columnes -->
    <table style="width: 100%; border-collapse: collapse;">
        <tr>
            <td style="width: 33.33%; padding-right: 10px; text-align: left; border-bottom: 1px solid #ccc;"><strong>ID:</strong> {ID_Recepte}</td>
            <td style="width: 33.33%; padding-left: 10px; text-align: left; border-bottom: 1px solid #ccc;"><strong>Data:</strong> {Data_formatejada}</td>
            <td style="width: 33.33%; padding-right: 10px; text-align: left; border-bottom: 1px solid #ccc;"><strong>Categoria:</strong> {Categoria}</td>
        </tr>
    </table>
    <!-- Segona fila: una columna -->
    <div style="padding-top: 10px; border-bottom: 1px solid #ccc; padding-bottom: 10px; margin-bottom: 10px;">
        <strong>Titol: </strong>{Titol}
    </div>
    <!-- Tercera fila: dos columnas con relación 80% - 20% -->
    <table style="width: 100%; border-collapse: collapse;">
        <tr>
            <!-- Columna de imagen (80%) -->
            <td style="width: 80%; padding: 10px; text-align: left; border: 1px solid #000;">
                <img src="data:image/jpeg;base64,{img_base64}" alt="Imagen" style="width: 100%; height: auto; border-radius: 5px;"/>
            </td>
            <!-- Columna de detalles (20%) dividida en tres filas con encabezados arriba -->
            <td style="width: 20%; padding: 0; text-align: left; border: 1px solid #000; height: 300px; vertical-align: top;">
                <table style="width: 100%; height: 100%; border-collapse: collapse;">
                    <tr style="height: 33.33%;">
                        <td style="border: 1px solid #000; padding: 10px; vertical-align: top;">
                            <strong>Temps:</strong> <br> {Temps}
                        </td>
                    </tr>
                    <tr style="height: 33.33%;">
                        <td style="border: 1px solid #000; padding: 10px; vertical-align: top;">
                            <strong>Ingredients:</strong> <br> {components}
                        </td>
                    </tr>
                    <tr style="height: 33.33%;">
                        <td style="border: 1px solid #000; padding: 10px; vertical-align: top;">
                            <strong>Categoria:</strong> <br> {Categoria}
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
    <!-- Quarta fila: una columna -->
    <div style="padding-top: 10px; padding-right: 10px; padding-left: 10px; border-bottom: 1px solid #ccc; padding-bottom: 10px; margin-bottom: 10px;">
        <strong>Metode:</strong>
        <p>{Metode}</p>
    </div>
    <!-- Quinta fila amb tres columnes -->
    <table style="width: 100%; border-collapse: collapse;">
        <tr>
            <td style="width: 33.33%; padding-right: 10px; text-align: left; border-bottom: 1px solid #ccc;"><strong>Temps:</strong> {Temps}</td>
            <td style="width: 33.33%; padding: 0 10px; text-align: left; border-bottom: 1px solid #ccc;"><strong>Ingredients: </strong> {components}</td>
            <td style="width: 33.33%; padding-left: 10px; text-align: right; border-bottom: 1px solid #ccc;"><strong>Categoria:</strong> {Categoria}</td>
        </tr>
    </table>
</div>
<!-- Separador -->
<div style="width: 100%; height: 2px; background-color: #123456; margin: 20px 0;"></div>
