import django_filters
from django import forms
from dtks.models import Kecamatan, Anggota
from penerima.models import Penerima

class KecamatanPenerimaFilter(django_filters.FilterSet):
    
    k = []
    
    for i in Kecamatan.objects.all().order_by('nama_kecamatan'):
        k.append((i.id,i.nama_kecamatan))
    
    
    kecamatan = django_filters.ChoiceFilter(
        choices=k, label="Kecamatan", empty_label="Semua", 
        widget=forms.Select(attrs={'class': 'form-control', 'style':'border-color: #063970;border-radius: 10px;color: #063970'})
    )
    class Meta:
    
        model=Penerima
        fields={
        }

# class KecamatanAnggotaFilter(django_filters.FilterSet):
#     k = []
    
#     for i in Kecamatan.objects.all().order_by('nama_kecamatan'):
#         k.append((i.id,i.nama_kecamatan))
    
    
#     kecamatan = django_filters.ChoiceFilter(
#         choices=k, label="Kecamatan", empty_label="Semua", 
#         widget=forms.Select(attrs={'class': 'form-control', 'style':'border-color: #063970;border-radius: 10px;color: #063970'})
#     )
#     class Meta:
        
    
#         model=Penerima
#         fields={
#         }