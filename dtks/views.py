from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Rumah, Aset, Kondisi_Rumah, Anggota, Kecamatan, Bansos
from penerima.models import Penerima, Ranking
from tablib import Dataset
import pandas as pd 
from django.contrib.auth import authenticate

from django.contrib.auth.decorators import login_required
from account.decorators import unauthenticated_user, allowed_users
from django.contrib import messages


# Create your views here.
@login_required(login_url='account:login')
def index(request):
  data_aset = Aset.objects.all()
  bansos = Bansos.objects.all()
  if request.user.groups.all()[0].name == "TKSK":
    base = 'base_tksk.html'
    data_rumah = Rumah.objects.filter(kecamatan__nama_kecamatan=request.user.location)
  else:
    base = 'base.html'
    data_rumah = Rumah.objects.all()
  context={
    'title': 'DTKS',
    'data_rumah': data_rumah,
    'bansos':bansos,
    'data_aset': data_aset,
    'base':base,
  }
  if request.method == 'POST' :
    dataset = Dataset()
    new_testing = request.FILES['file-excel-rt']
    data_import = dataset.load(new_testing.read(), format='xlsx')
    for data in data_import:
      coordinate = data[71]
      if coordinate is not None:
        coordinates = coordinate.split(",")
      if data[63]=='1':
        luas_lahan = 0
      else :
        luas_lahan = data[63]
      data_rumah = Rumah(
        IDJTG=data[0],
        nama_krt=data[15],
        kabupaten= data[6],
        kecamatan=Kecamatan.objects.get(nama_kecamatan=data[7]),
        desa=data[8],
        dusun=data[10],
        rt=data[11],
        rw=data[12],
        alamat=data[9],
        koordinat_lat = coordinates[0],
        koordinat_long = coordinates[1],
        jum_anggota = data[79]
      )
      data_rumah.save()
      if (data[47]==None):
        data_gas = 0
      else:
        data_gas = data[47]
      if (data[48]==None):
        data_kulkas = 0
      else:
        data_kulkas = data[48]
      if (data[49]==None):
        data_ac = 0
      else:
        data_ac = data[49]
      if (data[50]==None):
        data_pemanas_air = 0
      else:
        data_pemanas_air = data[50]
      if (data[51]==None):
        data_telepon_rumah = 0
      else:
        data_telepon_rumah = data[51]
      if (data[52]==None):
        data_tv = 0
      else:
        data_tv = data[52]
      if (data[53]==None):
        data_perhiasan = 0
      else:
        data_perhiasan = data[53]
      if (data[54]==None):
        data_komputer = 0
      else:
        data_komputer = data[54]
      if (data[55]==None):
        data_sepeda = 0
      else:
        data_sepeda = data[55]
      if (data[56]==None):
        data_motor = 0
      else:
        data_motor = data[56]
      if (data[57]==None):
        data_mobil = 0
      else:
        data_mobil = data[57]
      if (data[58]==None):
        data_perahu = 0
      else:
        data_perahu = data[58]
      if (data[59]==None):
        data_motor_tempel = 0
      else:
        data_motor_tempel = data[59]
      if (data[60]==None):
        data_perhau_motor = 0
      else:
        data_perhau_motor = data[60]
      if (data[61]==None):
        data_kapal = 0
      else:
        data_kapal = data[61]
      data_aset = Aset(
        rumah=data_rumah,
        gas=data_gas,
        kulkas=data_kulkas,
        ac=data_ac,
        pemanas_air=data_pemanas_air,
        telepon_rumah=data_telepon_rumah,
        tv=data_tv,
        perhiasan=data_perhiasan,
        komputer = data_komputer,
        sepeda = data_sepeda,
        motor = data_motor,
        mobil = data_mobil,
        perahu = data_perahu,
        motor_tempel = data_motor_tempel,
        perahu_motor = data_perhau_motor,
        kapal = data_kapal,
        lahan = luas_lahan,
        rumah_lain = data[64].split('#')[1],
        sapi = data[65],
        kerbau = data[66],
        kuda = data[67],
        babi = data[68],
        kambing = data[69],
        unggas = data[70],
        pengeluaran = data[46]
      )
      data_aset.save()
      data_kondisi = Kondisi_Rumah(
        rumah=data_rumah, 
        status_bangunan = data[23],
        luas_bangunan = data[24].split('#')[1],
        status_lahan = data[25],
        luas_lahan = data[26].split('#')[1],
        luas_lantai = data[27],
        jenis_lantai = data[28],
        jenis_dinding = data[29],
        kondisi_dinding = data[30],
        jenis_atap = data[31],
        kondisi_atap = data[32],
        jum_kamar = data[33],
        sumber_air = data[34],
        cara_air = data[36],
        sumber_penerangan = data[37],
        daya = data[38],
        id_pel = data[39],
        status_listrik = data[40],
        bahan_bakar = data[41],
        fasilitas_bab = data[43],
        jenis_kloset = data[44],
        buang_tinja = data[45],
        bansos_pusat = data[72],
        bansos_provinsi = data[73],
        bansos_kota = data[74],
        bansos_desa = data[75],
        bansos_lainnya = data[76],
        sumber_bansos = data[77],
      )
      data_kondisi.save()
      
  return render(request, 'dtks/index.html', context)

@login_required(login_url='account:login')
def input_form(request):
  if request.user.groups.all()[0].name == "TKSK":
    base = 'base_tksk.html'
  else:
    base = 'base.html'
  data_kecamatan = Kecamatan.objects.all()
  bansos = Bansos.objects.all()
  context={
    'title': 'Input KRT',
    'data_kecamatan' : data_kecamatan,
    'base':base,
    'bansos':bansos,
  }
  
  if request.method == 'POST':
    idjtg = request.POST['IDJTG']
    nama_krt = request.POST['nama_krt']
    kabupaten = request.POST['kabupaten']
    id_kecamatan = request.POST.get('kecamatan')
    kecamatan = Kecamatan.objects.get(id=id_kecamatan)
    desa = request.POST['desa']
    dusun = request.POST['dusun']
    rt = request.POST['rt']
    rw = request.POST['rw']
    alamat = request.POST['alamat']
    koordinat_lat = request.POST['koordinat_lat']
    koordinat_long = request.POST['koordinat_long']
    if koordinat_lat=="" and koordinat_long=="":
      koordinat_lat=None
      koordinat_long=None
    
    count_distinct_IDJTG = Rumah.objects.filter(IDJTG=idjtg).count()
    if count_distinct_IDJTG == 1:
      messages.error(request,'IDJTG sudah terdaftar')
    else:
      data_rumah = Rumah(IDJTG=idjtg,nama_krt=nama_krt,kabupaten=kabupaten,kecamatan=kecamatan,desa=desa,dusun=dusun,rt=rt,rw=rw,alamat=alamat,koordinat_lat = koordinat_lat,koordinat_long = koordinat_long,jum_anggota = 0)
      data_rumah.save()
    
      gas = request.POST['gas']
      kulkas = request.POST['kulkas']
      ac = request.POST['ac']
      pemanas_air = request.POST['pemanas_air']
      telepon_rumah = request.POST['telepon_rumah']
      tv = request.POST['tv']
      perhiasan = request.POST['perhiasan']
      komputer = request.POST['komputer']
      sepeda = request.POST['sepeda']
      motor = request.POST['motor']
      mobil = request.POST['mobil']
      perahu = request.POST['perahu']
      motor_tempel = request.POST['motor_tempel']
      perahu_motor = request.POST['perahu_motor']
      kapal = request.POST['kapal']
      lahan = request.POST['lahan']
      rumah_lain = request.POST['rumah_lain']
      sapi = request.POST['sapi']
      kerbau = request.POST['kerbau']
      kuda = request.POST['kuda']
      babi = request.POST['babi']
      kambing = request.POST['kambing']
      unggas = request.POST['unggas']
      pengeluaran = request.POST['pengeluaran']
      data_aset = Aset(
        rumah=data_rumah,
        gas=gas,
        kulkas=kulkas,
        ac=ac,
        pemanas_air=pemanas_air,
        telepon_rumah=telepon_rumah,
        tv=tv,
        perhiasan=perhiasan,
        komputer = komputer,
        sepeda = sepeda,
        motor = motor,
        mobil = mobil,
        perahu = perahu,
        motor_tempel = motor_tempel,
        perahu_motor = perahu_motor,
        kapal = kapal,
        lahan = lahan,
        rumah_lain = rumah_lain,
        sapi = sapi,
        kerbau = kerbau,
        kuda = kuda,
        babi = babi,
        kambing = kambing,
        unggas = unggas,
        pengeluaran = pengeluaran)
      data_aset.save()
        
      status_bangunan = request.POST['status_bangunan']
      luas_bangunan = request.POST['luas_bangunan']
      status_lahan = request.POST['status_lahan']
      luas_lahan = request.POST['luas_lahan']
      luas_lantai = request.POST['luas_lantai']
      jenis_lantai = request.POST['jenis_lantai']
      jenis_dinding = request.POST['jenis_dinding']
      kondisi_dinding = request.POST['kondisi_dinding']
      jenis_atap = request.POST['jenis_atap']
      kondisi_atap = request.POST['kondisi_atap']
      jum_kamar = request.POST['jum_kamar']
      sumber_air = request.POST['sumber_air']
      cara_air = request.POST['cara_air']
      sumber_penerangan = request.POST['sumber_penerangan']
      daya = request.POST['daya']
      id_pel = request.POST['id_pel']
      status_listrik = request.POST['status_listrik']
      bahan_bakar = request.POST['bahan_bakar']
      fasilitas_bab = request.POST['fasilitas_bab']
      jenis_kloset = request.POST['jenis_kloset']
      buang_tinja = request.POST['buang_tinja']
      bansos_pusat = request.POST.get('bansos_pusat', False)
      bansos_provinsi = request.POST.get('bansos_provinsi', False)
      bansos_kota = request.POST.get('bansos_kabupaten', False)
      bansos_desa = request.POST.get('bansos_desa', False)
      bansos_lainnya = request.POST.get('bansos_lainnya', False)
      sumber_bansos = request.POST.get('sumber_bansos')
      data_kondisi = Kondisi_Rumah(
        rumah=data_rumah, 
        status_bangunan = status_bangunan,
        luas_bangunan = luas_bangunan,
        status_lahan = status_lahan,
        luas_lahan = luas_lahan,
        luas_lantai = luas_lantai,
        jenis_lantai = jenis_lantai,
        jenis_dinding = jenis_dinding,
        kondisi_dinding = kondisi_dinding,
        jenis_atap = jenis_atap,
        kondisi_atap = kondisi_atap,
        jum_kamar = jum_kamar,
        sumber_air = sumber_air,
        cara_air = cara_air,
        sumber_penerangan = sumber_penerangan,
        daya = daya,
        id_pel = id_pel,
        status_listrik = status_listrik,
        bahan_bakar = bahan_bakar,
        fasilitas_bab = fasilitas_bab,
        jenis_kloset = jenis_kloset,
        buang_tinja = buang_tinja,
        bansos_pusat = bansos_pusat,
        bansos_provinsi = bansos_provinsi,
        bansos_kota = bansos_kota,
        bansos_desa = bansos_desa,
        bansos_lainnya = bansos_lainnya,
        sumber_bansos = sumber_bansos,
        )
      data_kondisi.save()
      id = data_rumah.id
      return HttpResponseRedirect(reverse('dtks:detail',args=(id,)))
  return render(request, 'dtks/input_form.html', context)

@login_required(login_url='account:login')
def detail(request, id):
  if request.user.groups.all()[0].name == "TKSK":
    base = 'base_tksk.html'
  else:
    base = 'base.html'
  data_rumah = Rumah.objects.get(id=id)
  id_rumah = data_rumah.id
  data_aset = Aset.objects.get(rumah=id_rumah)
  data_kondisi = Kondisi_Rumah.objects.get(rumah=id_rumah)
  data_anggota = Anggota.objects.filter(rumah=id_rumah)
  bansos = Bansos.objects.all()
  context={
    'base':base,
    'bansos':bansos,
    'title':'Detail KRT',
    'data_rumah'    : data_rumah,
    'data_aset'     : data_aset,
    'data_kondisi'  : data_kondisi,
    'data_anggota'  : data_anggota,
  }
  return render(request, 'dtks/rt.html', context)

@login_required(login_url='account:login')
def detail_art(request, id):
  if request.user.groups.all()[0].name == "TKSK":
    base = 'base_tksk.html'
  else:
    base = 'base.html'
  data_anggota = Anggota.objects.get(id=id)
  id_rumah = data_anggota.rumah_id
  bansos_list=Penerima.objects.filter(anggota_id=id).order_by('tahun')
  bansos = Bansos.objects.all()
  context={
    'base':base,
    'title':'Detail ART',
    'data_anggota' : data_anggota,
    'id_rumah'  : id_rumah,
    'bansos_list' : bansos_list,
    'bansos' : bansos,
  }
  return render(request, 'dtks/detail_art.html', context)

@login_required(login_url='account:login')
def input_art(request, id):
  if request.user.groups.all()[0].name == "TKSK":
    base = 'base_tksk.html'
  else:
    base = 'base.html'
  data_rumah = Rumah.objects.get(id=id)
  id = data_rumah.id
  
  if request.method == 'POST':
    idjtg_art = request.POST['idjtg_art']
    nama_art = request.POST['nama_art']
    nik = request.POST['nik']
    no_kk = request.POST['no_kk']
    ibu_kandung = request.POST['ibu_kandung']
    hubungan_krt = request.POST['hubungan_krt']
    hubungan_kk = request.POST['hubungan_kk']
    tempat_lahir = request.POST['tempat_lahir']
    tanggal_lahir = request.POST['tanggal_lahir']
    jenis_kelamin = request.POST['jenis_kelamin']
    status_perkawinan = request.POST['status_perkawinan']
    akta_nikah = request.POST['akta_nikah']
    tercantum_kk = request.POST['tercantum_kk']
    kepemilikan_kartu = request.POST['kepemilikan_kartu']
    status_kehamilan = request.POST['status_kehamilan']
    tgl_kehamilan = request.POST['tgl_kehamilan']
    jenis_disabilitas = request.POST['jenis_disabilitas']
    penyakit = request.POST['penyakit']
    sekolah = request.POST['sekolah']
    jenjang_pendidikan = request.POST['jenjang_pendidikan']
    kelas_tertinggi = request.POST['kelas_tertinggi']
    ijazah_tertinggi = request.POST['ijazah_tertinggi']
    status_bekerja = request.POST['status_bekerja']
    lapangan_usaha = request.POST['lapangan_usaha']
    status_kedudukan_kerja = request.POST['status_kedudukan_kerja']
    jenis_ketrampilan = request.POST['jenis_ketrampilan']
    # bansos_pusat = request.POST['bansos_pusat']
    bansos_provinsi = request.POST['bansos_provinsi']
    bansos_kota = request.POST['bansos_kabupaten']
    bansos_desa = request.POST['bansos_desa']
    bansos_lainnya = request.POST['bansos_lainnya']

    count_distinct_IDJTG_art = Anggota.objects.filter(IDJTG_ART=idjtg_art).count()
    count_distinct_nik = Anggota.objects.filter(nik=nik).count()
    if count_distinct_IDJTG_art == 1:
      messages.error(request,'IDJTG ART yang Anda masukkan sudah terdaftar')
      return redirect ('dtks:input_art', id)
    elif count_distinct_nik == 1:
      messages.error(request,'NIK yang Anda masukkan sudah terdaftar')
      return redirect ('dtks:input_art', id)
    else:
      data_anggota = Anggota(
        IDJTG_ART = idjtg_art,
        rumah = data_rumah,
        nama_art = nama_art,
        nik = nik,
        no_kk = no_kk,
        ibu_kandung = ibu_kandung,
        hubungan_krt = hubungan_krt,
        hubungan_kk = hubungan_kk,
        tempat_lahir = tempat_lahir,
        tanggal_lahir = tanggal_lahir,
        jenis_kelamin = jenis_kelamin,
        status_perkawinan = status_perkawinan,
        akta_nikah = akta_nikah,
        tercantum_kk = tercantum_kk,
        kepemilikan_kartu = kepemilikan_kartu,
        status_kehamilan = status_kehamilan,
        tgl_kehamilan = tgl_kehamilan,
        jenis_disabilitas = jenis_disabilitas,
        penyakit = penyakit,
        sekolah = sekolah,
        jenjang_pendidikan = jenjang_pendidikan,
        kelas_tertinggi = kelas_tertinggi,
        ijazah_tertinggi = ijazah_tertinggi,
        status_bekerja = status_bekerja,
        lapangan_usaha = lapangan_usaha,
        status_kedudukan_kerja = status_kedudukan_kerja,
        jenis_ketrampilan = jenis_ketrampilan,
        bansos_pusat = "0",
        bansos_provinsi = bansos_provinsi,
        bansos_kota = bansos_kota,
        bansos_desa = bansos_desa,
        bansos_lainnya = bansos_lainnya
        )
      data_anggota.save()
      messages.success(request,'Anggota baru berhasil ditambahkan!')
      count = data_rumah.jum_anggota
      data_rumah.jum_anggota = count+1
      data_rumah.save()
    return HttpResponseRedirect(reverse('dtks:detail',args=(id,)))
  
  bansos = Bansos.objects.all()
  context={
    'base': base,
    'data_rumah'  : data_rumah,
    'input_art'    : 'active',
    'bansos':bansos,
    'title':'Input ART',
    'button_submit': 'Tambah Data'
  }
  return render(request, 'dtks/input_art.html', context)

@login_required(login_url='account:login')
@allowed_users(allowed_roles=['Superadmin', 'Admin'])
def input_excel_art(request):
  if request.user.groups.all()[0].name == "TKSK":
    base = 'base_tksk.html'
  else:
    base = 'base.html'
  data_rumah = Rumah.objects.all()
  data_anggota = Anggota.objects.all()
  bansos = Bansos.objects.all()
  context={
    'title': 'DTKS',
    'data_rumah': data_rumah,
    'bansos':bansos,
    'title':'Login',
    'base':base
  }
  if request.method == 'POST' :
    dataset = Dataset()
    new_testing = request.FILES['file-excel-art']
    data_import = dataset.load(new_testing.read(), format='xlsx')
    for data in data_import:
      data_anggota = Anggota(
        IDJTG_ART = data[2],
        rumah = Rumah.objects.get(IDJTG=data[1]),
        nama_art = data[16],
        nik = data[15],
        no_kk = data[14],
        ibu_kandung = data[21],
        hubungan_krt = data[28],
        hubungan_kk = data[29],
        tempat_lahir = data[18],
        tanggal_lahir = data[17],
        jenis_kelamin = data[19],
        status_perkawinan = data[30],
        akta_nikah = data[31],
        tercantum_kk = data[32],
        kepemilikan_kartu = data[33],
        status_kehamilan = data[44],
        tgl_kehamilan = data[45],
        jenis_disabilitas = data[34],
        penyakit = data[35],
        sekolah = data[36],
        jenjang_pendidikan = data[37],
        kelas_tertinggi = data[38],
        ijazah_tertinggi = data[39],
        status_bekerja = data[40],
        lapangan_usaha = data[42],
        status_kedudukan_kerja = data[43],
        jenis_ketrampilan = data[51],
        bansos_pusat = "0",
        bansos_provinsi = data[47],
        bansos_kota = data[48],
        bansos_desa = data[49],
        bansos_lainnya = data[50],
      )
      data_anggota.save()
      dt_rumah = Rumah.objects.get(IDJTG=data[1])
      count = dt_rumah.jum_anggota
      dt_rumah.jum_anggota = count+1
      dt_rumah.save()
      
  return render(request, 'dtks/index.html', context)

#Edit Functions
@login_required(login_url='account:login')
def edit_krt(request, id):
  if request.user.groups.all()[0].name == "TKSK":
    base = 'base_tksk.html'
  else:
    base = 'base.html'
  data_kecamatan = Kecamatan.objects.all()
  data_rumah = Rumah.objects.get(id=id)
  id_rumah = data_rumah.id
  data_aset = Aset.objects.get(rumah=id_rumah)
  data_kondisi = Kondisi_Rumah.objects.get(rumah=id_rumah)
  bansos = Bansos.objects.all()
  context={
    'base':base,
    'bansos':bansos,
    'title': 'Edit KRT',
    'data_kecamatan' : data_kecamatan,
    'data_rumah' : data_rumah,
    'data_aset' : data_aset,
    'data_kondisi' : data_kondisi,
  }
  if request.method == 'POST':
    count_distinct_IDJTG = Rumah.objects.filter(IDJTG=request.POST['IDJTG']).count()
    idjtg = Rumah.objects.values_list('IDJTG', flat = True).get(id=id)
    if count_distinct_IDJTG == 1 and request.POST['IDJTG'] != idjtg :
      messages.error(request,'IDJTG sudah terdaftar')
      return redirect ('dtks:edit_krt', id)
    else:
      data_rumah.IDJTG = request.POST['IDJTG']
      data_rumah.nama_krt = request.POST['nama_krt']
      data_rumah.kabupaten = request.POST['kabupaten']
      id_kecamatan = request.POST.get('kecamatan')
      data_rumah.kecamatan = Kecamatan.objects.get(id=id_kecamatan)
      data_rumah.desa = request.POST['desa']
      data_rumah.dusun = request.POST['dusun']
      data_rumah.rt = request.POST['rt']
      data_rumah.rw = request.POST['rw']
      data_rumah.alamat = request.POST['alamat']
      data_rumah.koordinat_lat = request.POST['koordinat_lat']
      data_rumah.koordinat_long = request.POST['koordinat_long']
      data_rumah.save()
      
      data_aset.gas = request.POST['gas']
      data_aset.kulkas = request.POST['kulkas']
      data_aset.ac = request.POST['ac']
      data_aset.pemanas_air = request.POST['pemanas_air']
      data_aset.telepon_rumah = request.POST['telepon_rumah']
      data_aset.tv = request.POST['tv']
      data_aset.perhiasan = request.POST['perhiasan']
      data_aset.komputer = request.POST['komputer']
      data_aset.sepeda = request.POST['sepeda']
      data_aset.motor = request.POST['motor']
      data_aset.mobil = request.POST['mobil']
      data_aset.perahu = request.POST['perahu']
      data_aset.motor_tempel = request.POST['motor_tempel']
      data_aset.perahu_motor = request.POST['perahu_motor']
      data_aset.kapal = request.POST['kapal']
      data_aset.lahan = request.POST['lahan']
      data_aset.rumah_lain = request.POST['rumah_lain']
      data_aset.sapi = request.POST['sapi']
      data_aset.kerbau = request.POST['kerbau']
      data_aset.kuda = request.POST['kuda']
      data_aset.babi = request.POST['babi']
      data_aset.kambing = request.POST['kambing']
      data_aset.unggas = request.POST['unggas']
      data_aset.pengeluaran = request.POST['pengeluaran'] 
      data_aset.save()
        
      data_kondisi.status_bangunan = request.POST['status_bangunan']
      data_kondisi.luas_bangunan = request.POST['luas_bangunan']
      data_kondisi.status_lahan = request.POST['status_lahan']
      data_kondisi.luas_lahan = request.POST['luas_lahan']
      data_kondisi.luas_lantai = request.POST['luas_lantai']
      data_kondisi.jenis_lantai = request.POST['jenis_lantai']
      data_kondisi.jenis_dinding = request.POST['jenis_dinding']
      data_kondisi.kondisi_dinding = request.POST['kondisi_dinding']
      data_kondisi.jenis_atap = request.POST['jenis_atap']
      data_kondisi.kondisi_atap = request.POST['kondisi_atap']
      data_kondisi.jum_kamar = request.POST['jum_kamar']
      data_kondisi.sumber_air = request.POST['sumber_air']
      data_kondisi.cara_air = request.POST['cara_air']
      data_kondisi.sumber_penerangan = request.POST['sumber_penerangan']
      data_kondisi.daya = request.POST['daya']
      data_kondisi.id_pel = request.POST['id_pel']
      data_kondisi.status_listrik = request.POST['status_listrik']
      data_kondisi.bahan_bakar = request.POST['bahan_bakar']
      data_kondisi.fasilitas_bab = request.POST['fasilitas_bab']
      data_kondisi.jenis_kloset = request.POST['jenis_kloset']
      data_kondisi.buang_tinja = request.POST['buang_tinja']
      data_kondisi.bansos_pusat = request.POST.get('bansos_pusat', False)
      data_kondisi.bansos_provinsi = request.POST.get('bansos_provinsi', False)
      data_kondisi.bansos_kota = request.POST.get('bansos_kabupaten', False)
      data_kondisi.bansos_desa = request.POST.get('bansos_desa', False)
      data_kondisi.bansos_lainnya = request.POST.get('bansos_lainnya', False)
      data_kondisi.sumber_bansos = request.POST.get('sumber_bansos')
      data_kondisi.save()
      id = data_rumah.id
      return HttpResponseRedirect(reverse('dtks:detail',args=(id,)))
  return render(request, 'dtks/input_form.html', context)

@login_required(login_url='account:login')
def edit_art(request, id):
  if request.user.groups.all()[0].name == "TKSK":
    base = 'base_tksk.html'
  else:
    base = 'base.html'
  data_anggota = Anggota.objects.get(id=id)
  data_rumah = data_anggota.rumah
  tanggal_lahir = data_anggota.tanggal_lahir.strftime("%Y-%m-%d")
  bansos = Bansos.objects.all()
  context={
    'title': 'Edit ART',
    'base':base,
    'bansos':bansos,
    'data_anggota' : data_anggota,
    'data_rumah' : data_rumah,
    'tanggal_lahir' : tanggal_lahir,
    'button_submit':"Edit Data"
  }
  if request.method == 'POST':
    count_distinct_IDJTG_art = Anggota.objects.filter(IDJTG_ART=request.POST['idjtg_art']).count()
    count_distinct_nik = Anggota.objects.filter(nik=request.POST['nik']).count()
    idjtg_art = Anggota.objects.values_list('IDJTG_ART', flat = True).get(id=id)
    nik = Anggota.objects.values_list('nik', flat = True).get(id=id)
    if count_distinct_IDJTG_art == 1 and request.POST['idjtg_art'] != idjtg_art :
      messages.error(request,'IDJTG ART yang Anda masukkan sudah terdaftar')
      return redirect ('dtks:edit_art', id)
    elif count_distinct_nik == 1 and request.POST['nik'] != nik :
      messages.error(request,'NIK yang Anda masukkan sudah terdaftar')
      return redirect ('dtks:edit_art', id)
    else:
      data_anggota.IDJTG_ART = request.POST['idjtg_art']
      data_anggota.nama_art = request.POST['nama_art']
      data_anggota.nik = request.POST['nik']
      data_anggota.no_kk = request.POST['no_kk']
      data_anggota.ibu_kandung = request.POST['ibu_kandung']
      data_anggota.hubungan_krt = request.POST['hubungan_krt']
      data_anggota.hubungan_kk = request.POST['hubungan_kk']
      data_anggota.tempat_lahir = request.POST['tempat_lahir']
      data_anggota.tanggal_lahir = request.POST['tanggal_lahir']
      data_anggota.jenis_kelamin = request.POST['jenis_kelamin']
      data_anggota.status_perkawinan = request.POST['status_perkawinan']
      data_anggota.akta_nikah = request.POST['akta_nikah']
      data_anggota.tercantum_kk = request.POST['tercantum_kk']
      data_anggota.kepemilikan_kartu = request.POST['kepemilikan_kartu']
      data_anggota.status_kehamilan = request.POST['status_kehamilan']
      data_anggota.tgl_kehamilan = request.POST['tgl_kehamilan']
      data_anggota.jenis_disabilitas = request.POST['jenis_disabilitas']
      data_anggota.penyakit = request.POST['penyakit']
      data_anggota.sekolah = request.POST['sekolah']
      data_anggota.jenjang_pendidikan = request.POST['jenjang_pendidikan']
      data_anggota.kelas_tertinggi = request.POST['kelas_tertinggi']
      data_anggota.ijazah_tertinggi = request.POST['ijazah_tertinggi']
      data_anggota.status_bekerja = request.POST['status_bekerja']
      data_anggota.lapangan_usaha = request.POST['lapangan_usaha']
      data_anggota.status_kedudukan_kerja = request.POST['status_kedudukan_kerja']
      data_anggota.jenis_ketrampilan = request.POST['jenis_ketrampilan']
      data_anggota.bansos_provinsi = request.POST['bansos_provinsi']
      data_anggota.bansos_kota = request.POST['bansos_kabupaten']
      data_anggota.bansos_desa = request.POST['bansos_desa']
      data_anggota.bansos_lainnya = request.POST['bansos_lainnya']
      data_anggota.save()
      return HttpResponseRedirect(reverse('dtks:detail_art',args=(id,)))
  return render(request, 'dtks/input_art.html', context)  

#Delete Functions
def delete_krt(request, id):
  Rumah.objects.get(id=id).delete()
  return HttpResponseRedirect('/dtks/')

def delete_art(request, id, id_rumah):
  Anggota.objects.get(id=id).delete()
  data_rumah = Rumah.objects.get(id=id_rumah)
  count = data_rumah.jum_anggota
  data_rumah.jum_anggota = count-1
  data_rumah.save()
  return HttpResponseRedirect('/dtks/detail/'+id_rumah)

def anggota(request):
  if request.user.groups.all()[0].name == "TKSK":
    base = 'base_tksk.html'
    anggota = Ranking.objects.filter(anggota__rumah__kecamatan__nama_kecamatan=request.user.location)
    anggota_tolak = Ranking.objects.filter(anggota__rumah__kecamatan__nama_kecamatan=request.user.location).filter(status='Ditolak')
    anggota_disetujui = Ranking.objects.filter(anggota__rumah__kecamatan__nama_kecamatan=request.user.location).exclude(status='Ditolak').exclude( status='Belum Diverifikasi')
    anggota_pending = Ranking.objects.filter(anggota__rumah__kecamatan__nama_kecamatan=request.user.location).filter(status='Belum Diverifikasi')
  else:
    base = 'base.html'
    anggota = Ranking.objects.all()
    anggota_tolak = Ranking.objects.filter(status='Ditolak')
    anggota_disetujui = Ranking.objects.exclude(status='Ditolak').exclude( status='Belum Diverifikasi')
    anggota_pending = Ranking.objects.filter(status='Belum Diverifikasi')
  bansos = Bansos.objects.all()
  context ={
    'title': 'DTKS Anggota',
    'bansos': bansos,
    'anggota': anggota,
    'anggota_tolak': anggota_tolak,
    'anggota_disetujui': anggota_disetujui,
    'anggota_pending': anggota_pending,
    'base':base
  }
  return render(request, 'dtks/list_art.html', context)