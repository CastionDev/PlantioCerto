from rest_framework.test import APITestCase
from rest_framework import status
from .models import Cultura, ExigenciaClimatica, FaseLunarIdeal, CalendarioPlantio


class CulturaModelTest(APITestCase):

    def setUp(self):
        self.alface = Cultura.objects.create(
            nome_comum='Alface Crispa',
            nome_cientifico='Lactuca sativa',
            dias_colheita=60,
            tipo='hortaliça'
        )
        ExigenciaClimatica.objects.create(
            cultura=self.alface,
            temp_minima=10, temp_maxima=24,
            umidade_minima=60, umidade_maxima=90,
            chuva_minima_mm=50, chuva_maxima_mm=150
        )
        FaseLunarIdeal.objects.create(cultura=self.alface, fase_lua='crescente')
        CalendarioPlantio.objects.create(cultura=self.alface, regiao='sul', mes_inicio=3, mes_fim=7)

    def test_criacao_cultura(self):
        """Verifica se a cultura foi criada corretamente"""
        self.assertEqual(self.alface.nome_comum, 'Alface Crispa')
        self.assertEqual(self.alface.dias_colheita, 60)

    def test_relacionamento_exigencia_climatica(self):
        """Verifica se a exigência climática está vinculada corretamente"""
        self.assertEqual(self.alface.exigencia_climatica.temp_minima, 10)
        self.assertEqual(self.alface.exigencia_climatica.temp_maxima, 24)

    def test_relacionamento_fase_lunar(self):
        """Verifica se a fase lunar ideal está vinculada"""
        fases = self.alface.fases_lunares.values_list('fase_lua', flat=True)
        self.assertIn('crescente', fases)

    def test_str_cultura(self):
        """Verifica a representação em string do model"""
        self.assertEqual(str(self.alface), 'Alface Crispa')


class CulturaAPITest(APITestCase):

    def setUp(self):
        self.cultura = Cultura.objects.create(
            nome_comum='Rabanete',
            nome_cientifico='Raphanus sativus',
            dias_colheita=30,
            tipo='raiz'
        )

    def test_listar_culturas(self):
        """GET /api/culturas/ deve retornar lista com status 200"""
        response = self.client.get('/api/culturas/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_criar_cultura(self):
        """POST /api/culturas/ deve criar uma nova cultura"""
        dados = {
            'nome_comum': 'Cenoura',
            'nome_cientifico': 'Daucus carota',
            'dias_colheita': 90,
            'tipo': 'raiz'
        }
        response = self.client.post('/api/culturas/', dados, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Cultura.objects.count(), 2)