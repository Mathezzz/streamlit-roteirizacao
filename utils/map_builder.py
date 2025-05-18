# -*- coding: utf-8 -*-
"""
Created on Sun May 18 10:42:43 2025

@author: ander
"""

import folium

def create_route_map(coords: list[tuple[float, float]], route: list[int]) -> folium.Map:
    m = folium.Map(location=coords[0], zoom_start=12)
    folium.Marker(coords[0], icon=folium.Icon(color="green"), tooltip="Origem").add_to(m)
    for idx, pt in enumerate(coords[1:], start=1):
        folium.Marker(pt, icon=folium.Icon(color="red"), tooltip=f"Destino {idx}").add_to(m)
    path = [coords[i] for i in route]
    folium.PolyLine(path, weight=5, opacity=0.8).add_to(m)
    return m
