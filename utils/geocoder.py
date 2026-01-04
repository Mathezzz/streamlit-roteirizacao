import requests
import streamlit as st

class GeocodingError(Exception):
    pass

class LocationResolutionError(Exception):
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
        "input": str(address),
        "inputtype": "textquery",
        "fields": "geometry",
        "key": api_key,
        "language": "pt-BR"
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Streamlit App)"
    }

    response = requests.get(url, params=params, headers=headers, timeout=10)

    if response.status_code != 200:
        raise GeocodingError("Erro ao consultar o serviço de geocodificação.")

    data = response.json()
    print(data)
    candidates = data.get("candidates", [])

    if not candidates:
        raise GeocodingError("Endereço não encontrado.")

    location = candidates[0]["geometry"]["location"]
    lat = location["lat"]
    lon = location["lng"]

    return lat, lon

def resolve_location(input_str: str, api_key: str) -> tuple[float, float]:
    """
    Resolve uma localização a partir de:
    - coordenadas (lat, lon)
    - OU endereço em texto

    :param input_str: string digitada pelo usuário
    :param api_key: chave da API do Google
    :return: (lat, lon)
    """
    if not input_str or not input_str.strip():
        raise LocationResolutionError("Entrada vazia.")
    
    try:
        parts = input_str.split(",")
        if len(parts) != 2:
            raise ValueError

        lat = float(parts[0].strip())
        lon = float(parts[1].strip())

        if not (-90 <= lat <= 90 and -180 <= lon <= 180):
            raise ValueError

        return lat, lon

    except ValueError:
        pass

    try:
        return geocode_address(input_str, api_key)

    except GeocodingError as e:
        raise LocationResolutionError(str(e))