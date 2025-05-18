# -*- coding: utf-8 -*-
"""
Created on Sun May 18 10:42:43 2025

@author: ander
"""

import folium
import googlemaps
import polyline
import streamlit as st

def create_route_map(
    coords: list[tuple[float, float]],
    route: list[int]
) -> folium.Map:
    """
    Desenha no folium:
      - marcadores de origem (verde) e destinos (vermelho);
      - para cada par consecutivo na rota, obtém o polyline da Directions API
        e traça no mapa (usando linha real de estrada).
    """
    # Inicializa mapa centralizado na origem
    m = folium.Map(location=coords[0], zoom_start=12)
    folium.Marker(coords[0], icon=folium.Icon(color="green"), tooltip="Origem").add_to(m)
    for idx, pt in enumerate(coords[1:], start=1):
        folium.Marker(pt, icon=folium.Icon(color="red"), tooltip=f"Destino {idx}").add_to(m)

    # Cliente GoogleMaps
    gmaps = googlemaps.Client(key=st.secrets["google"]["api_key"])

    # Para cada trecho da rota otimizada
    for i in range(len(route) - 1):
        a = coords[route[i]]
        b = coords[route[i + 1]]

        # Chama Directions API
        directions = gmaps.directions(
            origin=a,
            destination=b,
            mode="driving",
            departure_time="now"
        )

        # Extrai polyline de overview
        if directions and "overview_polyline" in directions[0]:
            poly_str = directions[0]["overview_polyline"]["points"]
            points = polyline.decode(poly_str)  # lista de (lat, lon)

            # Desenha a linha real no mapa
            folium.PolyLine(points, weight=5, opacity=0.8).add_to(m)
        else:
            # fallback: linha reta
            folium.PolyLine([a, b], weight=2, color="gray", dash_array="5,5").add_to(m)

    return m