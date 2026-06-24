from rest_framework import serializers
from .models import Cultura, ExigenciaClimatica, FaseLunarIdeal, CalendarioPlantio


class ExigenciaClimaticaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExigenciaClimatica
        fields = ['temp_minima', 'temp_maxima', 'umidade_minima', 'umidade_maxima', 'chuva_minima_mm', 'chuva_maxima_mm']


class FaseLunarIdealSerializer(serializers.ModelSerializer):
    class Meta:
        model = FaseLunarIdeal
        fields = ['fase_lua']


class CalendarioPlantioSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalendarioPlantio
        fields = ['regiao', 'mes_inicio', 'mes_fim']


class CulturaSerializer(serializers.ModelSerializer):
    exigencia_climatica = ExigenciaClimaticaSerializer(read_only=True)
    fases_lunares        = FaseLunarIdealSerializer(many=True, read_only=True)
    calendarios           = CalendarioPlantioSerializer(many=True, read_only=True)

    class Meta:
        model = Cultura
        fields = ['id', 'nome_comum', 'nome_cientifico', 'dias_colheita', 'tipo', 'exigencia_climatica', 'fases_lunares', 'calendarios']