import requests
from .geocoding import obter_coordenadas

def obter_localizacao(cep: str) -> dict:
    cep = cep.replace("-", "").strip()

    response = requests.get(f"https://viacep.com.br/ws/{cep}/json/")
    response.raise_for_status()
    dados = response.json()

    if "erro" in dados:
        raise ValueError(f"CEP {cep} não encontrado.")

    cidade = dados["localidade"]
    estado = dados["uf"]
    coordenadas = obter_coordenadas(cidade, estado)

    return {
        "cidade": cidade,
        "estado": estado,
        "regiao": obter_regiao(estado),
        "latitude": coordenadas["latitude"],
        "longitude": coordenadas["longitude"],
    }

def obter_regiao(uf: str) -> str:
    regioes = {
        "norte":        ["AM", "PA", "AC", "RO", "RR", "AP", "TO"],
        "nordeste":     ["MA", "PI", "CE", "RN", "PB", "PE", "AL", "SE", "BA"],
        "centro-oeste": ["MT", "MS", "GO", "DF"],
        "sudeste":      ["SP", "RJ", "MG", "ES"],
        "sul":          ["PR", "SC", "RS"],
    }
    for regiao, ufs in regioes.items():
        if uf.upper() in ufs:
            return regiao
    return "desconhecida"