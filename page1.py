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
if "n_destinos" not in st.session_state:
    st.session_state["n_destinos"] = 1


with st.expander("Breve tutorial"):
    st.write('''
        No primeiro campo de entrada coloque o ponto de Origem, de onde sairia a carga
        
        Formato esperado: (lat, long) Exemplo: -23.5505, -46.6333
        
        ---
        
        
        No segundo campo de entrada, coloque os pontos de destino.
        
        Adicione mais pontos separando as coordenadas de lat, long com ";"
        
        Formato esperado: (lat1, long1; lat2, long2, lat3, long3)
        
        Exemplo: -23.5510, -46.6400; -23.5600, -46.6200
    ''')
    st.write("🚚")

st.subheader("Destinos")

col1, col2 = st.columns(2)

with col1:
    if st.button("Adicionar destino"):
        if st.session_state["n_destinos"] < 7:
            st.session_state["n_destinos"] += 1

with col2:
    if st.button("Remover destino"):
        if st.session_state["n_destinos"] > 1:
            st.session_state["n_destinos"] -= 1

st.write(f"Quantidade de destinos: {st.session_state["n_destinos"]}")

# Inputs
origem = st.text_input("Origem (lat, lon)", key="input_origem")

for i in range(st.session_state["n_destinos"]):
    st.text_input(f"Destino {i+1}", key=f"destino_{i}")

def get_destinos_from_state():
    destinos = []
    for i in range(st.session_state["n_destinos"]):
        value = st.session_state.get(f"destino_{i}", "")

        if value is None:
            continue
        
        value = value.strip()
        if value:
            destinos.append(value)
    return destinos

def calcular_rota():

    destinos = get_destinos_from_state()
    if len(destinos) == 0:
        st.toast("Nenhum destino informado.", icon="⚠️")
    
    try:
        coords = [tuple(map(float, origem.split(",")))]
    except Exception:
        st.toast("Origem inválida. Informe a origem com o formato: lat,long", icon="⚠️")
    try:
        destinos_coords = parse_coords(";".join(destinos))
        coords += destinos_coords

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
        st.toast("Formato dos destinos inválidos. Cheque se os destinos possuem formato: lat,long", icon="⚠️")


# Botão que dispara o cálculo
st.button("Calcular rota", on_click=calcular_rota)

# Se deu erro
if st.session_state["erro"]:
    st.error(f"Erro: {st.session_state['erro']}")

# Mostrar resultados se a rota foi calculada
if st.session_state["rota_calculada"]:
    st.success("Rota calculada com sucesso!")
    st.write("🔀 **Ordem otimizada de visita:**", " → ".join(map(str, st.session_state["route"])))
    
    # Recriar o mapa no momento da visualização
    m = create_route_map(st.session_state["coords"], st.session_state["route"])
    st_folium(m, width=700, height=500)

    if st.button("🔁 Limpar rota"):
        for key in ["coords", "route", "rota_calculada", "erro"]:
            st.session_state.pop(key, None)
        
        for key in list(st.session_state.keys()):
            if key.startswith("dest_"):
                st.session_state.pop(key)

        st.session_state["n_destinos"] = 1
