import requests
import streamlit as st

class GeocodingError(Exception):
    pass

def geocode_address(address: str, api_key: str) -> tuple[float, float]:
    """
    Resolve um endereço em texto para latitude e longitude usando Google Places.

    :param address: Endereço em texto livre
    :param api_key: Chave da API do Google
    :return: (lat, lon)
    """
    url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"

    if not address or not address.strip():
        raise GeocodingError("Endereço vazio.")

    params = {
        "input": address,
        "inputtype": "textquery",
        "fields": "geometry",
        "key": api_key,
    }

    response = requests.get(url, params=params, timeout=200)

    if response.status_code != 200:
        raise GeocodingError("Erro ao consultar o serviço de geocodificação.")

    data = response.json()

    candidates = data.get("candidates", [])

    if not candidates:
        raise GeocodingError("Endereço não encontrado.")

    location = candidates[0]["geometry"]["location"]
    lat = location["lat"]
    lon = location["lng"]

    return lat, lon