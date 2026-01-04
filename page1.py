# -*- coding: utf-8 -*-
"""
Created on Sun May 18 10:43:23 2025

@author: ander
"""

import streamlit as st
from streamlit_folium import st_folium

from utils.geocoder import resolve_location
from utils.parser import parse_coords
from utils.distance import build_distance_matrix
from utils.solver import solve_tsp
from utils.map_builder import create_route_map
from utils.destino_validator import resolve_destinos_individuais

st.set_page_config("Roteirização", layout="wide")
st.title("Roteirização Logística 🗺️📍🚚")

# Inicializar estados
if "rota_calculada" not in st.session_state:
    st.session_state["rota_calculada"] = False
if "erro" not in st.session_state:
    st.session_state["erro"] = None
if "n_destinos" not in st.session_state:
    st.session_state["n_destinos"] = 1
if "destino_erros" not in st.session_state:
    st.session_state["destino_erros"] = {}


with st.expander("Breve tutorial"):
    st.write('''
        ## Origem
        No primeiro campo de entrada coloque o ponto de Origem, de onde sairia a carga
        
        Formato esperado: Endereço ou (lat, long) Exemplo: Avenida Alberto Maranhão, 100, Mossoró; Ou: -23.5505, -46.6333
        
        ---
        
        ## Destinos
        Então, utilizando os botões "Adicionar destino" e "Remover destino", defina quantos destinos deseja dar entrada
        
        Nos campos de entrada criados, coloque os pontos de destino.
        
        Formato esperado em cada linha: Endereço ou (lat, long) Exemplo: Avenida Alberto Maranhão, 100, Mossoró; Ou: -23.5505, -46.6333

        - Linhas em branco serão ignoadas        
    ''')
    st.write("🚚")

# Inputs
origem = st.text_input("Origem: Digite sua localização ou passe uma lat, long", key="input_origem")

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

for i in range(st.session_state["n_destinos"]):
    st.text_input(f"Destino {i+1}", key=f"destino_{i}")

    erro = st.session_state.get("destino_erros", {}).get(i)
    if erro:
        st.caption(f"⚠️ {erro}")

def get_destinos_from_state():
    destinos = []
    for i in range(st.session_state["n_destinos"]):
        key = f"destino_{i}"
        value = st.session_state.get(key, "")

        if value and value.strip():
            destinos.append({
                "index": i,
                "label": f"Destino {i+1}",
                "value": value.strip()
            })
    return destinos

def calcular_rota():

    st.session_state["destino_erros"] = {}

    _origem = [{"index": 0, "label": "input_origem", "value": origem}]
    origem_result = resolve_destinos_individuais(_origem)

    if not origem_result["ok"]:
        st.toast(f"Origem: {origem_result['error']}", icon="⚠️")
        return

    origem_coords = origem_result["coords"]

    destinos = get_destinos_from_state()
    if len(destinos) == 0:
        st.toast("Nenhum destino informado.", icon="⚠️")

    resultado_destinos = resolve_destinos_individuais(destinos)    
    
    if not resultado_destinos["ok"]:
        for erro in resultado_destinos["errors"]:
            st.session_state["destino_erros"][erro["index"]] = erro["error"]
        return
    
    try:
        coords = origem_coords + resultado_destinos["coords"]

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
# if st.session_state["erro"]:
#     st.error(f"Erro: {st.session_state['erro']}")

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
