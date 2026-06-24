from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .models import Usuario
from .serializers import UsuarioSerializer


class CadastroView(generics.CreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [permissions.AllowAny]  # qualquer um pode se cadastrar


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def meu_perfil(request):
    serializer = UsuarioSerializer(request.user)
    return Response(serializer.data)