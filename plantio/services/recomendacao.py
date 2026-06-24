from datetime import date
from culturas.models import Cultura
from .clima import obter_clima
from .lua import obter_fase_lunar

def recomendar_culturas(latitude: float, longitude: float, regiao: str) -> list:
    clima      = obter_clima(latitude, longitude)
    fase_lunar = obter_fase_lunar()
    mes_atual  = date.today().month

    temperatura = clima["temperatura"]
    umidade     = clima["umidade"]
    chuva       = clima["chuva_mm"]

    culturas = Cultura.objects.prefetch_related(
        "exigencia_climatica",
        "fases_lunares",
        "calendarios"
    ).all()

    resultado = []

    for cultura in culturas:
        pontuacao = 0
        motivos   = []

        try:
            ex = cultura.exigencia_climatica
        except Exception:
            continue

        if ex.temp_minima <= temperatura <= ex.temp_maxima:
            pontuacao += 3
            motivos.append("temperatura ideal")

        if ex.umidade_minima <= umidade <= ex.umidade_maxima:
            pontuacao += 2
            motivos.append("umidade ideal")

        if ex.chuva_minima_mm <= chuva <= ex.chuva_maxima_mm:
            pontuacao += 2
            motivos.append("precipitação adequada")

        fases_ideais = cultura.fases_lunares.values_list("fase_lua", flat=True)
        if fase_lunar in fases_ideais:
            pontuacao += 2
            motivos.append(f"lua {fase_lunar} favorável")

        na_epoca = cultura.calendarios.filter(
            regiao=regiao,
            mes_inicio__lte=mes_atual,
            mes_fim__gte=mes_atual
        ).exists()
        if na_epoca:
            pontuacao += 3
            motivos.append("época certa do ano")

        if pontuacao > 0:
            resultado.append({
                "cultura":   cultura.nome_comum,
                "tipo":      cultura.tipo,
                "pontuacao": pontuacao,
                "motivos":   motivos,
            })

    return sorted(resultado, key=lambda x: x["pontuacao"], reverse=True)