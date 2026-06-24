from rest_framework import serializers
from .models import Usuario


class UsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'password', 'cep', 'cidade', 'estado', 'regiao']

    def create(self, validated_data):
        usuario = Usuario(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            cep=validated_data.get('cep', ''),
            cidade=validated_data.get('cidade', ''),
            estado=validated_data.get('estado', ''),
            regiao=validated_data.get('regiao', ''),
        )
        usuario.set_password(validated_data['password'])  # criptografa a senha
        usuario.save()
        return usuario