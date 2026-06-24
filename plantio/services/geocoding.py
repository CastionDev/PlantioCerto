import requests

def obter_coordenadas(cidade: str, estado: str) -> dict:
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": f"{cidade}, {estado}, Brasil",
        "format": "json",
        "limit": 1,
    }
    headers = {
        "User-Agent": "PlantioCerto/1.0"  # a Nominatim exige um User-Agent identificável
    }

    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    dados = response.json()

    if not dados:
        raise ValueError(f"Não foi possível localizar coordenadas para {cidade}, {estado}.")

    return {
        "latitude": float(dados[0]["lat"]),
        "longitude": float(dados[0]["lon"]),
    }