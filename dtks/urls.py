from django.urls import path
from . import views

app_name = 'dtks'
urlpatterns = [
    path('', views.index, name='index'),
    path('anggota', views.anggota, name='anggota'),
    path('input', views.input_form, name='input_form'),
    path('detail/<int:id>', views.detail, name='detail'),
    path('edit/<int:id>', views.edit_krt, name='edit_krt'),
    path('delete/<int:id>', views.delete_krt, name='delete_krt'),
    path('detail_art/<int:id>', views.detail_art, name='detail_art'),
    path('input_art/<int:id>', views.input_art, name='input_art'),
    path('input_excel_art', views.input_excel_art, name='input_excel_art'),
    path('delete_art/<int:id>/<str:id_rumah>', views.delete_art, name='delete_art'),
    path('edit_art/<int:id>', views.edit_art, name='edit_art'),
    # path('cekdata', views.index, name='index'),
]

