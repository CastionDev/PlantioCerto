import ephem
from datetime import date

def obter_fase_lunar(data: date = None) -> str:
    if data is None:
        data = date.today()

    lua = ephem.Moon(str(data))
    iluminacao = lua.phase  # 0 a 100

    if iluminacao < 10:
        return "nova"
    elif iluminacao < 50:
        return "crescente"
    elif iluminacao < 90:
        return "cheia"
    else:
        return "minguante"