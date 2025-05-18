# -*- coding: utf-8 -*-
"""
Created on Sun May 18 10:43:23 2025

@author: ander
"""

import streamlit as st
from streamlit_folium import st_folium
from utils.parser import parse_coords
from utils.distance import build_distance_matrix
from utils.solver import solve_tsp
from utils.map_builder import create_route_map

st.set_page_config("Roteirização", layout="wide")
st.title("Roteirização Logística")

# Inicializar estados
if "rota_calculada" not in st.session_state:
    st.session_state["rota_calculada"] = False
if "erro" not in st.session_state:
    st.session_state["erro"] = None

# Inputs
origem = st.text_input("Origem (lat, lon)", key="input_origem")
destinos = st.text_area("Destinos (lat, lon separados por ';')", key="input_destinos")

def calcular_rota():
    try:
        coords = [tuple(map(float, origem.split(",")))] + parse_coords(destinos)
        matrix = build_distance_matrix(coords, st.secrets["google"]["api_key"])
        route = solve_tsp(matrix)

        # Guardar apenas dados simples no session_state
        st.session_state["coords"] = coords
        st.session_state["route"] = route
        st.session_state["rota_calculada"] = True
        st.session_state["erro"] = None

    except Exception as e:
        st.session_state["rota_calculada"] = False
        st.session_state["erro"] = str(e)

# Botão que dispara o cálculo
st.button("Calcular rota", on_click=calcular_rota)

# Se deu erro
if st.session_state["erro"]:
    st.error(f"Erro: {st.session_state['erro']}")

# Mostrar resultados se a rota foi calculada
if st.session_state["rota_calculada"]:
    st.write("🔀 **Ordem otimizada de visita:**", " → ".join(map(str, st.session_state["route"])))
    
    # Recriar o mapa no momento da visualização
    m = create_route_map(st.session_state["coords"], st.session_state["route"])
    st_folium(m, width=700, height=500)

    if st.button("🔁 Limpar rota"):
        for key in ["coords", "route", "rota_calculada", "erro"]:
            st.session_state.pop(key, None)
        st.experimental_rerun()
