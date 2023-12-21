from django.urls import path
from . import views

app_name = 'mapping'
urlpatterns = [  
    path('', views.index, name='index'),
    path('bansos', views.bansos, name='bansos'),
    path('kecamatan', views.kecamatan, name='kecamatan'),
    path('delete_bansos/<int:id>', views.delete_bansos, name='delete_bansos'),
    path('update_bansos/<int:id>', views.update_bansos, name='update_bansos'),
    path('delete_kecamatan/<int:id>', views.delete_kecamatan, name='delete_kecamatan'),
    path('update_kecamatan/<int:id>', views.update_kecamatan, name='update_kecamatan'),
]