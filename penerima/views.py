from django.shortcuts import render, redirect
from dtks.models import Anggota, Bansos, Kecamatan
from .models import Penerima, Ranking
from .filters import TahunFilter
from django.contrib.auth.decorators import login_required
from account.decorators import unauthenticated_user, allowed_users
from datetime import datetime
from django.http import HttpResponse, JsonResponse
import json

# Create your views here.
def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

@login_required(login_url='account:login')
def index(request, slug):
    nama_bansos = Bansos.objects.get(slug=slug)
    if request.user.groups.all()[0].name == "TKSK":
        base = 'base_tksk.html'
        penerima = Penerima.objects.filter(anggota__rumah__kecamatan__nama_kecamatan=request.user.location).filter(bansos__slug__contains=slug)
    else:
        base = 'base.html'
        penerima = Penerima.objects.filter(bansos__slug__contains=slug)

    bansos = Bansos.objects.all()
    
    context={
        'title':'Daftar Penerima',
        'penerima':penerima,
        'base':base,
        'bansos':bansos,
        'nama_bansos' : nama_bansos
    }
    return render(request, 'penerima/index.html', context)

@login_required(login_url='account:login')
def detail(request, id):
    penerima = Penerima.objects.get(id=id)
    bansos = Bansos.objects.all()
    jumlah_menerima = Penerima.objects.filter(anggota=penerima.anggota.id).filter(bansos__nama_bansos=penerima.bansos).count()
    # bansos=Penerima.objects.filter(anggota_id=id).order_by('tahun')
    if request.user.groups.all()[0].name == "TKSK":
        base = 'base_tksk.html'
    else:
        base = 'base.html'
    context={
        'title':'Detail Penerima',
        'base':base,
        # 'data_anggota': anggota,
        'penerima':penerima,
        'bansos':bansos,
        'jumlah_menerima':jumlah_menerima
        
    }
    return render(request, 'penerima/detail_penerima.html', context)

def daterange(start, end, step=1):
        current_year = start
        while current_year <= end:
            yield current_year
            current_year += step

@login_required(login_url='account:login')
@allowed_users(allowed_roles=['Superadmin', 'Admin'])
def ranking(request, slug, tahun):
    # tahun_filter=TahunFilter(request.POST, queryset=Ranking.objects.all().order_by('status'))
    # ranking=tahun_filter.qs
    ranking=Ranking.objects.filter(bansos__slug=slug).filter(tahun=tahun).order_by('-nilai')
    belum_diverifikasi = Ranking.objects.filter(bansos__slug=slug).filter(tahun=tahun).filter(status='Belum Diverifikasi').count()
    disetujui = Ranking.objects.filter(bansos__slug=slug).filter(tahun=tahun).filter(status='Disetujui').count()
    penerima = Ranking.objects.filter(bansos__slug=slug).filter(tahun=tahun).filter(status='Penerima').count()
    bansos = Bansos.objects.all()
    kuota = Bansos.objects.values_list('kuota', flat=True).get(slug=slug)
    nama_bansos = Bansos.objects.get(slug=slug)
    t = []
            
    for year in daterange(2021, datetime.now().year):
        t.append(year)
    context={
        'title': 'Verifikasi Data Anggota',
        'ranking':ranking,
        'belum_diverifikasi':belum_diverifikasi,
        'penerima':penerima,
        'bansos':bansos,
        'slug':slug,
        'kuota': int(kuota),
        'disetujui':disetujui,
        't':t,
        'nama_bansos': nama_bansos
        # 'form':tahun_filter.form,
    }
    return render(request, 'penerima/ranking.html', context)

def disetujui(request, id):
    if request.method == 'POST':
        ranking = Ranking.objects.get(id=id)
        ranking.status = 'Disetujui'
        ranking.save()
        return redirect ('penerima:ranking',slug=ranking.bansos.slug, tahun=ranking.tahun)

def tolak(request):
    if is_ajax(request):
        # alasan = request.POST.get('alasan', False)
        alasan = json.loads(request.POST.get('alasan'))
        id = json.loads(request.POST.get('id'))
        ranking = Ranking.objects.get(id=id)
        ranking.status = 'Ditolak'
        ranking.alasan = alasan
        ranking.save()
        return JsonResponse({'data': id})

def ditolak(request, id):
    if request.method == 'POST':
        ranking = Ranking.objects.get(id=id)
        ranking.status = 'Ditolak'
        ranking.save()
        return redirect ('penerima:ranking',slug=ranking.bansos.slug, tahun=ranking.tahun)
    
def proses(request, slug):
    if request.method == 'POST':
        jenis_bansos = Bansos.objects.get(slug=slug)
        calon_penerima = Ranking.objects.filter(bansos=jenis_bansos).filter(status='Disetujui')[:int(jenis_bansos.kuota)]
        for r in calon_penerima :
            
            ranking = Ranking.objects.get(id=r.id)
            ranking.status = 'Penerima'
            ranking.save()
            penerima = Penerima(
                anggota = Anggota.objects.get(id=r.anggota.id),
                bansos = Bansos.objects.get(nama_bansos=r.bansos),
                tahun = r.tahun
            )
            penerima.save()
        return redirect ('penerima:index', slug=r.bansos.slug)
    
def proses_ranking(request):
    bansos = Bansos.objects.all()
    sembako_lansia_tahun_ini = Ranking.objects.filter(bansos__nama_bansos='Sembako Lansia').filter(tahun=datetime.now().year).count()
    sembako_disabilitas_tahun_ini = Ranking.objects.filter(bansos__nama_bansos='Sembako Disabilitas').filter(tahun=datetime.now().year).count()
    alat_bantu_tahun_ini = Ranking.objects.filter(bansos__nama_bansos='Alat Bantu Disabilitas').filter(tahun=datetime.now().year).count()
    anggota = Anggota.objects.all()
    context={
        'title':'Proses Perankingan',
        'bansos': bansos,
        'sembako_lansia_tahun_ini':sembako_lansia_tahun_ini,
        'sembako_disabilitas_tahun_ini':sembako_disabilitas_tahun_ini,
        'alat_bantu_tahun_ini': alat_bantu_tahun_ini,
        'anggota':anggota
    }
    return render(request, 'penerima/ranking_proses.html', context)

def ranking_proses(request, slug):
    anggota = Anggota.objects.all()
    if request.method == 'POST':
        for anggota in anggota:
            ranking = Ranking(
                anggota = Anggota.objects.get(id=anggota.id),
                bansos = Bansos.objects.get(slug = slug),
                tahun = datetime.now().year
                # datetime.now().year
            )
            ranking.save()
        return redirect ('penerima:ranking',slug=slug, tahun = datetime.now().year)
    
