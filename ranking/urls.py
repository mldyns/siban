from django.urls import path
from . import views

app_name = 'ranking'
urlpatterns = [
    path('<str:slug>/<int:tahun>', views.index, name='index'),
    path('delete_kriteria/<str:slug>/<int:id>//<int:tahun>', views.delete_kriteria, name='delete_kriteria'),
    path('edit_bobot/<str:slug>/<int:id>/<int:tahun>', views.edit_bobot, name='edit_bobot'),
    path('update_kriteria/<str:slug>/<int:id>/<int:tahun>', views.update_kriteria, name='update_kriteria'),
    path('simpan_ranking/<str:slug>/<int:tahun>', views.simpan_ranking, name='simpan_ranking'),
    path('delete_ranking/<str:slug>/<int:tahun>', views.delete_ranking, name='delete_ranking'),
]