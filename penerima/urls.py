from django.urls import path
from . import views

app_name = 'penerima'
urlpatterns = [
    path('<str:slug>', views.index, name='index'),
    path('detail/<int:id>', views.detail, name='detail'),
    path('ranking/<str:slug>/<int:tahun>', views.ranking, name='ranking'),
    path('ranking/disetujui/<int:id>/', views.disetujui, name='disetujui'),
    path('ranking/ditolak/<int:id>/', views.ditolak, name='ditolak'),
    path('ranking/proses', views.proses_ranking, name='proses_ranking'),
    path('ranking/proses/<str:slug>', views.ranking_proses, name='ranking_proses'),
    path('proses/<str:slug>', views.proses, name='proses'),
    path('tolak/', views.tolak, name='tolak'),
]