from django.urls import path
from . import views

app_name = 'clustering'
urlpatterns = [
    path('', views.index, name='index'),
    path('proses', views.proses, name='proses'),
    path('c/<str:name>', views.c, name='c'),
    path('analisis_cluster', views.analisis_cluster, name='analisis_cluster'),
    path('hasil', views.hasil, name='hasil'),
    path('delete/<str:name>', views.delete, name='delete'),
    path('dtks/<str:idjtg>', views.dtks, name='dtks'),
]