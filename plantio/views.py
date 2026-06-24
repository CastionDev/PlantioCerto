from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .services.viacep import obter_localizacao
from .services.clima import obter_clima
from .services.lua import obter_fase_lunar
from .services.recomendacao import recomendar_culturas


@api_view(['GET'])
def recomendacao_por_cep(request):
    cep = request.query_params.get('cep')

    if not cep:
        return Response({"erro": "Informe o parâmetro 'cep'."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        localizacao = obter_localizacao(cep)
    except ValueError as e:
        return Response({"erro": str(e)}, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return Response({"erro": "Erro ao consultar localização."}, status=status.HTTP_502_BAD_GATEWAY)

    try:
        recomendacoes = recomendar_culturas(
            localizacao["latitude"],
            localizacao["longitude"],
            localizacao["regiao"]
        )
    except Exception as e:
        return Response({"erro": f"Erro ao gerar recomendação: {str(e)}"}, status=status.HTTP_502_BAD_GATEWAY)

    return Response({
        "localizacao": localizacao,
        "fase_lunar": obter_fase_lunar(),
        "recomendacoes": recomendacoes,
    })


@api_view(['GET'])
def clima_atual(request):
    latitude = request.query_params.get('latitude')
    longitude = request.query_params.get('longitude')

    if not latitude or not longitude:
        return Response({"erro": "Informe 'latitude' e 'longitude'."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        clima = obter_clima(float(latitude), float(longitude))
    except Exception:
        return Response({"erro": "Erro ao consultar o clima."}, status=status.HTTP_502_BAD_GATEWAY)

    return Response(clima)