from rest_framework.test import APITestCase
from rest_framework import status
from .models import Usuario


class UsuarioAPITest(APITestCase):

    def test_cadastro_usuario(self):
        """POST /api/cadastro/ deve criar um novo usuário"""
        dados = {
            'username': 'mariaagricultora',
            'email': 'maria@email.com',
            'password': 'senha123',
            'cep': '88010-001',
            'cidade': 'Florianópolis',
            'estado': 'SC',
            'regiao': 'sul'
        }
        response = self.client.post('/api/cadastro/', dados, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Usuario.objects.count(), 1)

    def test_senha_nao_aparece_na_resposta(self):
        """A senha nunca deve ser retornada na resposta da API"""
        dados = {'username': 'teste', 'password': 'senha123'}
        response = self.client.post('/api/cadastro/', dados, format='json')
        self.assertNotIn('password', response.data)

    def test_login_usuario(self):
        """POST /api/login/ deve retornar tokens de acesso"""
        Usuario.objects.create_user(username='joao', password='senha123')

        response = self.client.post('/api/login/', {
            'username': 'joao',
            'password': 'senha123'
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_perfil_sem_autenticacao_retorna_401(self):
        """GET /api/perfil/ sem token deve ser bloqueado"""
        response = self.client.get('/api/perfil/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_perfil_com_autenticacao(self):
        """GET /api/perfil/ com token válido deve retornar dados do usuário"""
        usuario = Usuario.objects.create_user(username='joao', password='senha123')

        login = self.client.post('/api/login/', {
            'username': 'joao', 'password': 'senha123'
        }, format='json')
        token = login.data['access']

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get('/api/perfil/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'joao')