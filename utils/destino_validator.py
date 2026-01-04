import streamlit as st
from utils.geocoder import resolve_location

def resolve_destinos_individuais(destinos):
    coords = []
    erros = []

    for destino in destinos:
        resultado = resolve_location(destino["value"], st.secrets["google"]["api_key"])

        if not resultado["ok"]:
            erros.append({
                "index": destino["index"],
                "error": resultado["error"]
            })
        else:
            coords.append(resultado["coords"])

    if erros:
        return {
            "ok": False,
            "errors": erros
        }

    return {
        "ok": True,
        "coords": coords
    }
