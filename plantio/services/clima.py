import requests

def obter_clima(latitude: float, longitude: float) -> dict:
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude":          latitude,
        "longitude":         longitude,
        "current":           ["temperature_2m", "relative_humidity_2m", "precipitation"],
        "daily":             ["precipitation_sum"],
        "timezone":          "America/Sao_Paulo",
        "forecast_days":     1,
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    dados = response.json()

    return {
        "temperatura": dados["current"]["temperature_2m"],
        "umidade":     dados["current"]["relative_humidity_2m"],
        "chuva_mm":    dados["daily"]["precipitation_sum"][0],
    }