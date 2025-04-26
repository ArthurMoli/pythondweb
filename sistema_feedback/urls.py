from django.contrib import admin
from django.urls import path, include
from avaliacoes.views import register  # Certifique-se de importar a função de registro

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('avaliacoes.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', register, name='register'),
]