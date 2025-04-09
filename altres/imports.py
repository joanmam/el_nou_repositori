import base64
import html
import io
import os
import re
import sys
import uuid
from datetime import date, datetime, timedelta
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
from bs4 import BeautifulSoup
from selenium import webdriver
import streamlit as st
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from altres.funcions import create_thumbnail2
from altres.funcions import convertir_a_blob
from altres.funcions import dataframe_externs
import pyshorteners
from altres.funcions import dataframe_estadistiques
from pathlib import Path
from altres.funcions import barra_lateral2
from altres.funcions import generar_html_fontawesome2
import json
import locale
from urllib.parse import urlparse
from altres.funcions import assignar_imatge
from altres.diccionari import diccionari_imatges


