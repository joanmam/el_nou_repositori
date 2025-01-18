import sys
import os


sys.path.append(os.path.join(os.path.dirname(__file__), 'pages'))

import streamlit as st

import pages.crear as crear
import pages.visualizar as visualizar
import pages.ingredients as ingredients
import pages.filtrar as filtrar
from pages.visualizar import create_card, get_image_base64




st.title("Hola")







