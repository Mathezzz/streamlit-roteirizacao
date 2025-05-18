# -*- coding: utf-8 -*-
"""
Created on Sun May 18 10:38:36 2025

@author: ander
"""

def parse_coords(text: str, sep: str = ";") -> list[tuple[float, float]]:
    """Converte 'lat,lon; lat,lon; …' em lista de tuplas."""
    coords = []
    for part in text.split(sep):
        part = part.strip()
        if part:
            lat, lon = part.split(",")
            coords.append((float(lat), float(lon)))
    return coords
