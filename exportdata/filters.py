import django_filters
from django import forms
from dtks.models import Bansos, Kecamatan
from penerima.models import Penerima

class PenerimaFilter(django_filters.FilterSet):
    b = []
    k = []
    t = []
    for i in Penerima.objects.values_list('tahun', flat=True).order_by('tahun').distinct():
        t.append((i,i))
    for i in Bansos.objects.all().order_by('nama_bansos'):
        b.append((i.id,i.nama_bansos))
    for i in Kecamatan.objects.all().order_by('nama_kecamatan'):
        k.append((i.id,i.nama_kecamatan))
    
    
    tahun = django_filters.ChoiceFilter(
        choices=t, label="Tahun", empty_label="Semua", 
        widget=forms.Select(attrs={'class': 'form-control', 'style':'border-color: #063970;border-radius: 10px;color: #063970'})
    )
    bansos = django_filters.ChoiceFilter(
        choices=b, label="Jenis Bantuan Sosial", empty_label="Semua",
        widget=forms.Select(attrs={'class': 'form-control', 'style':'border-color: #063970;border-radius: 10px;color: #063970'})
    )
    anggota__rumah__kecamatan = django_filters.ChoiceFilter(
        choices=k, label="Kecamatan", empty_label="Semua",
        widget=forms.Select(attrs={'class': 'form-control', 'style':'border-color: #063970;border-radius: 10px;color: #063970'})
    )
    class Meta:
        
    
        model=Penerima
        fields={
        }