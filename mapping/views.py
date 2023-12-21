from django.shortcuts import render, redirect
from django.db.models import Avg
from dtks.models import Anggota, Kecamatan, Bansos, Rumah
from penerima.models import Penerima
from mapping.filters import PenerimaFilter
from django.contrib.auth.decorators import login_required
from account.decorators import unauthenticated_user, allowed_users

import geocoder
import folium
from folium.plugins import HeatMap
from folium.plugins import FastMarkerCluster
from geopy.geocoders import Nominatim
import pandas as pd
from django_pandas.io import read_frame

geolocator = Nominatim(user_agent="bytescout", timeout=None)

def getloc_lats_longs(locations):
    loc_lats_longs = []
    for loc in locations:
        loc_lat_long = geolocator.geocode(query = loc+', Purbalingga')
        count = Anggota.objects.filter(rumah__kecamatan__nama_kecamatan = loc).count()
        loc_lats_longs.append([loc_lat_long.latitude, loc_lat_long.longitude, count])
    return loc_lats_longs
 
# Create your views here.
@login_required(login_url='account:login')
def index(request):
    #tahun=Penerima.objects.values_list("tahun", flat=True).order_by("tahun").distinct()
    kecamatan = Kecamatan.objects.all()
    bansos = Bansos.objects.all()
    anggota = Anggota.objects.all()
    penerima = Penerima.objects.all()
    nama_kecamatan = Kecamatan.objects.values_list('nama_kecamatan', flat=True)
    avg_lat = Penerima.objects.aggregate(avg=Avg('anggota__rumah__koordinat_lat'))['avg']
    avg_long = Penerima.objects.aggregate(avg=Avg('anggota__rumah__koordinat_long'))['avg']

    #Create Map Object
    if penerima :
        m = folium.Map(location=[avg_lat, avg_long], zoom_start= 12)
    else :
        m = folium.Map(location=[-7.28, 109.35], zoom_start= 12)
    
    #cluster marker
    # latitudes = [ang.rumah.koordinat_lat for ang in anggota]
    # longitudes = [ang.rumah.koordinat_long for ang in anggota]
    # FastMarkerCluster(data=list(zip(latitudes, longitudes))).add_to(m)

    #Map Heat
    latitudes = [ang.rumah.koordinat_lat for ang in anggota]
    longitudes = [ang.rumah.koordinat_long for ang in anggota]
    HeatMap(data=list(zip(latitudes, longitudes)), radius=50, blur=20).add_to(m)
    # lats_longs = getloc_lats_longs(nama_kecamatan)
    # HeatMap(lats_longs, radius=40, blur=20).add_to(m)
    
    #filter
    penerima_filter=PenerimaFilter(request.POST, queryset=Penerima.objects.all())
    penerima_query=penerima_filter.qs

    # df = read_frame(penerima_query, fieldnames=['id', 'anggota__nama_art', 'anggota__rumah__koordinat_lat', 'anggota__rumah__koordinat_long'])
    # dfg = df.groupby(['anggota__rumah__koordinat_lat', 'anggota__rumah__koordinat_long']).agg(lambda x: list(x)).reset_index()
    
    # for row in dfg.itertuples() :
    #     nama = row.anggota__nama_art
    # image_name='bansos.jpg'
    # image=static('mapping/leaflet/images/')+image_name
    #marker anggota
    # for marker in anggota:
    #     folium.Marker([marker.rumah.koordinat_lat, marker.rumah.koordinat_long]).add_to(m)
    #marker penerima
    
    for marker in penerima_query:
        if marker.status == 'Diterima':
            garis = '<hr style="border: solid green 4px;opacity: 100;margin-top:10px; margin-bottom:10px;width: 150px;">'
        else :
            garis = '<hr style="border: solid yellow 4px;opacity: 100;margin-top:10px; margin-bottom:10px;width: 150px;">'
        folium.Marker([marker.anggota.rumah.koordinat_lat, marker.anggota.rumah.koordinat_long], tooltip='Click for more',
                        popup='<b>Nama : </b>'+marker.anggota.nama_art+'<br>'+'<b>Kecamatan : </b>'+marker.anggota.rumah.kecamatan.nama_kecamatan+
                        '<br><b>Desa : </b>'+marker.anggota.rumah.desa+'<br><b>Bansos : </b>'+marker.bansos.nama_bansos+'<br><b>Status : </b>'+marker.status+garis+'<a href="#">Detail',
                        icon=folium.Icon(color=marker.bansos.color, icon='')).add_to(m)
        #get HTML representation of map object
    m = m._repr_html_()
    if request.user.groups.all()[0].name == "TKSK":
        base = 'base_tksk.html'
    else:
        base = 'base.html'
    context={
    'title': 'Mapping',
    'm' : m,
    'kecamatan':kecamatan,
    # 'tahun':tahun,
    'bansos':bansos,
    'form':penerima_filter.form,
    'base':base
    }
    return render (request, 'mapping/index.html', context)

@login_required(login_url='account:login')
@allowed_users(allowed_roles=['Superadmin', 'Admin'])
def bansos(request):
    bansos = Bansos.objects.all()
    if request.method == 'POST':
        nama = request.POST.get('nama')
        kuota = request.POST.get('kuota')
        warna = request.POST.get('warna')
        new_bansos = Bansos(nama_bansos=nama,kuota=kuota,color=warna)
        new_bansos.save()
        return redirect ('mapping:bansos')
    context={
        'bansos':bansos,
        'title':'Data Bansos',
    }
    return render(request, 'mapping/bansos.html', context)

def delete_bansos(request, id):
    Bansos.objects.filter(id=id).delete()
    return redirect('mapping:bansos')

def update_bansos(request, id):
  
    if request.method == 'POST':
        newnama = request.POST['newnama']
        newkuota = request.POST['newkuota']
        newwarna = request.POST['newwarna']
        bansos = Bansos.objects.get(id=id)
        bansos.nama_bansos = newnama
        bansos.kuota = newkuota
        bansos.color = newwarna
        # bansos.set_password(newpassword)
        bansos.save()
        return redirect ('mapping:bansos')

@login_required(login_url='account:login')
@allowed_users(allowed_roles=['Superadmin', 'Admin'])
def kecamatan(request):
    bansos = Bansos.objects.all()
    kecamatan = Kecamatan.objects.all()
    if request.method == 'POST':
        nama = request.POST['nama']
        kecamatan = Kecamatan(nama_kecamatan=nama)
        kecamatan.save()
        return redirect ('mapping:kecamatan')
    context={
       'bansos':bansos,
       'kecamatan':kecamatan,
       'title':'Data Kecamatan',
    }
    return render(request, 'mapping/kecamatan.html', context)

def delete_kecamatan(request, id):
    Kecamatan.objects.filter(id=id).delete()
    return redirect('mapping:kecamatan')

def update_kecamatan(request, id):
    if request.method == 'POST':
        nama = request.POST['nama']
        kecamatan = Kecamatan.objects.get(id=id)
        kecamatan.nama_kecamatan = nama
        kecamatan.save()
        return redirect ('mapping:kecamatan')
    