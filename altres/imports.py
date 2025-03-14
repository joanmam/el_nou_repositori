import base64
import html
import io
import os
import re
import sys
import uuid
from datetime import date, datetime
from io import BytesIO, StringIO

import emoji
import pandas as pd
import requests
import sqlitecloud
import streamlit as st
import streamlit.components.v1 as components
from jinja2.sandbox import unsafe
from PIL import Image
from streamlit import date_input

from altres.funcions import (agregar_estilos_css, agregar_iconos_google,
                             background_home, banner, connexio,
                             convert_blob_to_base64, convert_blob_to_image,
                             convert_image_to_base64, crear_tarjeta_html,
                             crear_tarjeta_html_fet, crear_tarjeta_html_pas,
                             crear_tarjeta_html_protocol,
                             crear_tarjeta_html_resumida,
                             crear_taula_encapcalat,
                             crear_taula_passos_sense_encapcalat,
                             create_thumbnail, create_thumbnail2, cropping,
                             dataframe_accions, dataframe_actualitzar,
                             dataframe_pagina, dataframe_passos, estils_marc,
                             find_url, inici, lletra_variable, obtenir_emoji,
                             obtenir_ingredients, process_observacions,
                             rellotge, row_style, separador)
from altres.variables import cami_db, img_url
from altres.funcions import procesar_fila
from altres.funcions import convert_blob_to_base64_2
from altres.funcions import agregar_espaciado_css
from altres.funcions import generar_targeta
from altres.funcions import generar_html_fontawesome
from altres.funcions import font_awesome