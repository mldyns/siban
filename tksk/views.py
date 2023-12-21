from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from dtks.models import Anggota, Bansos, Kecamatan, Rumah, Aset, Kondisi_Rumah
from penerima.models import Penerima, Ranking
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from account.decorators import unauthenticated_user, allowed_users


# Create your views here.
@login_required(login_url='account:login')
def index(request):
    bansos_disabilitas = Bansos.objects.get(nama_bansos='Sembako Disabilitas')
    bansos_lansia = Bansos.objects.get(nama_bansos='Sembako Lansia')
    alat_bantu = Bansos.objects.get(nama_bansos='Alat Bantu Disabilitas')

    
    disabilitas_penerima = Ranking.objects.filter(anggota__rumah__kecamatan__nama_kecamatan=request.user.location).filter(bansos=bansos_disabilitas).filter(status='Penerima').count()
    disabilitas_disetujui = Ranking.objects.filter(anggota__rumah__kecamatan__nama_kecamatan=request.user.location).filter(bansos=bansos_disabilitas).filter(status="Disetujui").count()
    count_disabilitas_diterima = disabilitas_penerima + disabilitas_disetujui
    count_disabilitas_ditolak = Ranking.objects.filter(anggota__rumah__kecamatan__nama_kecamatan=request.user.location).filter(bansos=bansos_disabilitas).filter(status="Ditolak").count()
    lansia_penerima = Ranking.objects.filter(bansos=bansos_lansia).filter(status='Penerima').count()
    lansia_disetujui = Ranking.objects.filter(anggota__rumah__kecamatan__nama_kecamatan=request.user.location).filter(bansos=bansos_lansia).filter(status="Disetujui").count()
    count_lansia_diterima = lansia_penerima + lansia_disetujui
    count_lansia_ditolak = Ranking.objects.filter(anggota__rumah__kecamatan__nama_kecamatan=request.user.location).filter(bansos=alat_bantu).filter(status="Ditolak").count()
    alat_bantu_penerima = Ranking.objects.filter(bansos=alat_bantu).filter(status='Penerima').count()
    alat_bantu_disetujui = Ranking.objects.filter(anggota__rumah__kecamatan__nama_kecamatan=request.user.location).filter(bansos=alat_bantu).filter(status="Disetujui").count()
    count_alat_bantu_diterima = alat_bantu_penerima + alat_bantu_disetujui
    count_alat_bantu_ditolak = Ranking.objects.filter(anggota__rumah__kecamatan__nama_kecamatan=request.user.location).filter(bansos=alat_bantu).filter(status="Ditolak").count()
    jumlah_pmks = Anggota.objects.all().count()
    
    bansos = Bansos.objects.all()
    tahun = Penerima.objects.values_list('tahun', flat=True).distinct()

    penerima = []
    for p in tahun:
        count = Penerima.objects.filter(anggota__rumah__kecamatan__nama_kecamatan=request.user.location).filter(tahun = p).distinct().count()
        penerima.append(count)
    pmks = []
    for p in tahun:
        count = Ranking.objects.filter(anggota__rumah__kecamatan__nama_kecamatan=request.user.location).filter(tahun = p).distinct().count()
        pmks.append(count)


    context={
        'bansos':bansos,
        'title': 'Dashboard TKSK',
        'penerima' : penerima,
        'pmks':pmks,
        'tahun':tahun,
        'count_pmks':jumlah_pmks,
        'count_disabilitas_diterima':count_disabilitas_diterima,
        'count_disabilitas_ditolak':count_disabilitas_ditolak,
        'count_lansia_diterima':count_lansia_diterima,
        'count_alat_bantu_ditolak':count_alat_bantu_ditolak,
        'count_alat_bantu_diterima':count_alat_bantu_diterima,
        'count_lansia_ditolak':count_lansia_ditolak,
    }
    return render (request, 'tksk/index.html', context)

@login_required(login_url='account:login')
def input(request):
    data_rumah = Rumah.objects.filter(kecamatan__nama_kecamatan=request.user.location)
    data_aset = Aset.objects.all()
    bansos = Bansos.objects.all()
    context={
        'bansos':bansos,
        'title': 'DTKS',
        'data_rumah': data_rumah,
        'data_aset': data_aset
    }
    return render (request, 'tksk/input.html', context)

@login_required(login_url='account:login')
def upload_bukti(request):
    penerima_list = Penerima.objects.filter(anggota__rumah__kecamatan__nama_kecamatan=request.user.location).filter(status='Dalam Proses')
    bansos = Bansos.objects.all()
    anggota=Anggota.objects.all()

    if request.method == 'POST':
        id = request.POST['id']
        bukti = request.FILES['bukti']
        penerima = Penerima.objects.get(id=id)
        penerima.foto_bukti = bukti
        penerima.status = 'Diterima'
        penerima.save()
        messages.success(request, 'Upload bukti berhasil!')
        return redirect('tksk:upload_bukti')
    context={
        'bansos':bansos,
        'title': 'Upload Bukti',
        'penerima':penerima_list,
        'anggota':anggota,
    }
    return render(request, 'tksk/upload_bukti.html', context)