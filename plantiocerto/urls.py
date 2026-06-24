from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('plantio.urls')),
    path('api/', include('culturas.urls')),
    path('api/', include('usuarios.urls')),
]