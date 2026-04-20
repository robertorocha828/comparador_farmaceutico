from django.urls import path
from . import views

urlpatterns = [
    path('', views.subir_archivos, name='subir_archivos'),
    path('subir_archivos/', views.subir_archivos, name='subir_archivos_alt'),
    path('resultado/<int:proceso_id>/', views.ver_resultados, name='ver_resultados'),
]