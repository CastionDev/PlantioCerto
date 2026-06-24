from unittest.mock import patch
from rest_framework.test import APITestCase
from rest_framework import status
from culturas.models import Cultura, ExigenciaClimatica, FaseLunarIdeal, CalendarioPlantio
from .services.recomendacao import recomendar_culturas


class RecomendacaoServiceTest(APITestCase):

    def setUp(self):
        self.alface = Cultura.objects.create(
            nome_comum='Alface Crispa', dias_colheita=60, tipo='hortaliça'
        )
        ExigenciaClimatica.objects.create(
            cultura=self.alface,
            temp_minima=10, temp_maxima=24,
            umidade_minima=60, umidade_maxima=90,
            chuva_minima_mm=0, chuva_maxima_mm=200
        )
        FaseLunarIdeal.objects.create(cultura=self.alface, fase_lua='crescente')
        CalendarioPlantio.objects.create(cultura=self.alface, regiao='sul', mes_inicio=1, mes_fim=12)

    @patch('plantio.services.recomendacao.obter_fase_lunar')
    @patch('plantio.services.recomendacao.obter_clima')
    def test_recomendacao_pontuacao_maxima(self, mock_clima, mock_lua):
        """Cultura que atende todos os critérios deve ter pontuação alta"""
        mock_clima.return_value = {'temperatura': 15, 'umidade': 70, 'chuva_mm': 50}
        mock_lua.return_value = 'crescente'

        resultado = recomendar_culturas(-27.59, -48.55, 'sul')

        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0]['cultura'], 'Alface Crispa')
        self.assertEqual(resultado[0]['pontuacao'], 12)  # 3+2+2+2+3

    @patch('plantio.services.recomendacao.obter_fase_lunar')
    @patch('plantio.services.recomendacao.obter_clima')
    def test_recomendacao_temperatura_fora_da_faixa(self, mock_clima, mock_lua):
        """Cultura não deve pontuar em temperatura se estiver fora da faixa ideal"""
        mock_clima.return_value = {'temperatura': 40, 'umidade': 70, 'chuva_mm': 50}
        mock_lua.return_value = 'crescente'

        resultado = recomendar_culturas(-27.59, -48.55, 'sul')

        self.assertNotIn('temperatura ideal', resultado[0]['motivos'])


class RecomendacaoEndpointTest(APITestCase):

    def test_recomendacao_sem_cep_retorna_erro(self):
        """Endpoint deve retornar 400 se o CEP não for informado"""
        response = self.client.get('/api/recomendacao/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_clima_sem_coordenadas_retorna_erro(self):
        """Endpoint de clima deve retornar 400 sem latitude/longitude"""
        response = self.client.get('/api/clima/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)