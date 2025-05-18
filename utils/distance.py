# -*- coding: utf-8 -*-
"""
Created on Sun May 18 10:41:04 2025

@author: ander
"""

import googlemaps
import streamlit as st

api_key = st.secrets["google"]["api_key"]

def build_distance_matrix(
    coords: list[tuple[float, float]],
    api_key: str
) -> list[list[int]]:
    """Retorna matriz de distâncias (m) entre todos os pares via Google Maps."""
    gmaps = googlemaps.Client(key=api_key)
    n = len(coords)
    matrix = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                res = gmaps.distance_matrix(coords[i], coords[j], mode="driving")
                matrix[i][j] = res["rows"][0]["elements"][0]["distance"]["value"]
    return matrix
