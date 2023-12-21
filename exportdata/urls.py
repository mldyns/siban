from django.urls import path
from . import views

app_name = 'exportdata'
urlpatterns = [
    path('', views.index, name='index'),
    path('export', views.export, name='export'),
    # path('cekdata', views.index, name='index'),
]