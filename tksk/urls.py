from django.urls import path
from . import views

app_name = 'tksk'
urlpatterns = [
    path('dashboard', views.index, name='dashboard'),
    path('input', views.input, name='input'),
    path('upload_bukti', views.upload_bukti, name='upload_bukti')
]