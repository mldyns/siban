# Create your views here.
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.conf.urls.static import static
from dtks.models import Rumah, Aset, Kondisi_Rumah, Anggota, Bansos
from penerima.models import Penerima, Ranking
from .models import Kriteria, Crips
from django.http import HttpResponseRedirect
from datetime import datetime

def daterange(start, end, step=1):
        current_year = start
        while current_year <= end:
            yield current_year
            current_year += step

def index(request,slug,tahun):
    excluded_fields_kriteria1 = ["id", "rumah"]
    excluded_fields_kriteria2 = ["id", "rumah"]
    excluded_fields_kriteria3 = ["id", "rumah", "penerima", "ranking", "IDJTG_ART", "nama_art", "nik", "no_kk"]
    kriteria1 = [f.name for f in Kondisi_Rumah._meta.get_fields() if f.name not in excluded_fields_kriteria1]
    kriteria3 = [f.name for f in Aset._meta.get_fields() if f.name not in excluded_fields_kriteria3]
    kriteria2 = [f.name for f in Anggota._meta.get_fields() if f.name not in excluded_fields_kriteria2]

    # list_kondisi_rumah = Kondisi_Rumah.objects.all()
    # list_aset = Aset.objects.all()
    # list_anggota = Anggota.objects.all()
    usia = "usia"
    tgl = "tanggal_lahir"

    kriteria2 = [usia if item == tgl else item for item in kriteria2]
    
    disabilitas = "disabilitas"
    jenis = "jenis_disabilitas"

    kriteria2 = [disabilitas if item == jenis else item for item in kriteria2]

    # penghasilan = "penghasilan"
    # pengeluaran = "pengeluaran"

    # kriteria3 = [penghasilan if item == pengeluaran else item for item in kriteria3]

    nama_kriteria = kriteria1+kriteria2+kriteria3
    bansos = Bansos.objects.all()
    penerima = Penerima.objects.filter(bansos__slug__contains=slug)
    get_bansos = Bansos.objects.get(slug=slug)
    kriteria = Kriteria.objects.filter(bansos=get_bansos, tahun=tahun)
    nama_k = Kriteria.objects.values_list('nama_kriteria', flat=True).filter(bansos=get_bansos,tahun=tahun).distinct()
    get_kriteria = ['nama_art']
    for k in nama_k:
        get_kriteria.append(k)
    if request.method == 'POST':
        nama = request.POST.get('nama_kriteria')
        bobot = request.POST.get('bobot')
        atribut = request.POST.get('atribut')
        new_kriteria = Kriteria(nama_kriteria=nama,bobot=bobot,atribut=atribut,bansos=get_bansos, tahun=tahun)
        new_kriteria.save()
        crips = globals()[nama] 
        for c in crips :
            new_crips = Crips(kriteria = new_kriteria,nama_crips = c,bobot_crips = 0,bansos=get_bansos)
            new_crips.save()
    data_crips = Crips.objects.all()
    data_normalisasi = []
    data_normalisasi1 = []
    data_normalisasi2 = []
    data_hasil = []
    data_hasil_sorted = []
    anggota = Anggota.objects.all()
    anggota_ranking = Ranking.objects.filter(bansos__slug=slug, tahun=tahun)
    if not anggota_ranking:        
        for d in anggota:
            nama = d.nama_art
            anggota = Anggota.objects.get(id=d.id)
            # hasil = d.get('nilai_akhir')
            data_ranking=Ranking(anggota = anggota,
                                status="Diranking",
                                tahun=tahun,
                                bansos=get_bansos,
                                alasan="",
                                nilai=0)
            data_ranking.save()
    else:
        #PROSES NORMALISASI
        for a in anggota_ranking:
            nama=a.anggota.nama_art
            id=a.anggota.id
            rumah = a.anggota.rumah
            nilai_akhir=[]
            
            data_kriteria = {'id':id,'nama_art':nama}
            data_kriteria1 = {'id':id,'nama_art':nama}
            data_kriteria2 = {'id':id,'nama_art':nama}
            data_hitung = {'id':id, 'nama_art':nama}
            data_normalisasi.append(data_kriteria)
            data_normalisasi1.append(data_kriteria1)
            data_normalisasi2.append(data_kriteria2)
            for c in nama_k:
                # print("CEK"+c)
                k = Kriteria.objects.get(nama_kriteria=c,bansos=get_bansos,tahun=tahun)
                if c in kriteria1:
                    # print("kondisi rumh")
                    kondisi=Kondisi_Rumah.objects.values_list(c, flat=True).get(rumah=rumah)
                elif c in kriteria2:
                    if c == 'usia' :
                        c = 'tanggal_lahir'
                        kondisi=Anggota.objects.values_list(c, flat=True).get(rumah=rumah, id=id)
                        c = 'usia'
                    elif c == 'disabilitas' :
                        c = 'jenis_disabilitas'
                        kondisi=Anggota.objects.values_list(c, flat=True).get(rumah=rumah, id=id)
                        c = 'disabilitas'
                    else :
                        kondisi=Anggota.objects.values_list(c, flat=True).get(rumah=rumah, id=id)
                else :
                    # print("aset rumh")
                    # if c == 'penghasilan' :
                    #     c = 'pengeluaran'
                    kondisi=Aset.objects.values_list(c, flat=True).get(rumah=rumah)
                    # c = 'penghasilan'
                # kondisi2=Kondisi_Rumah.objects.values_list(c, flat=True).get(rumah=rumah)

                if c == 'luas_bangunan' :
                    if kondisi < 50 :
                        kondisi = '<50 m2'
                    elif kondisi >= 50 and kondisi <= 75:
                        kondisi = '50-75 m2'
                    elif kondisi >= 76 and kondisi <= 100:
                        kondisi = '76-100 m2'
                    else :
                        kondisi = '>100 m2'
                elif c == 'luas_lahan' :
                    if kondisi < 9 :
                        kondisi = '<9 m2'
                    elif kondisi >= 9 and kondisi <= 13:
                        kondisi = '9-13 m2'
                    elif kondisi >= 14 and kondisi <= 17:
                        kondisi = '14-17 m2'
                    elif kondisi >= 18 and kondisi <= 25:
                        kondisi = '18-25 m2'
                    else:
                        kondisi = '>25 m2'
                elif c == 'luas_lahan' :
                    if kondisi < 8 :
                        kondisi = '<8 m2'
                    elif kondisi >= 8 and kondisi <= 12:
                        kondisi = '8-12 m2'
                    elif kondisi >= 13 and kondisi <= 16:
                        kondisi = '13-16 m2'
                    elif kondisi >= 17 and kondisi <= 24:
                        kondisi = '17-24 m2'
                    else:
                        kondisi = '>24 m2'
                elif c == 'usia' :
                    tahun_lahir = kondisi.year
                    tahun_sekarang = datetime.now().year
                    usia = tahun_sekarang - tahun_lahir
                    if usia < 65:
                        kondisi = '<65'
                    else:
                        kondisi = '>=65'
                elif c == 'sekolah' :
                    if kondisi == 'Masih sekolah' :
                        kondisi = 'Masih sekolah'
                    else:
                        kondisi = 'Tidak sekolah'
                elif c == 'penyakit' :
                    if kondisi == 'Tidak ada' :
                        kondisi = 'Tidak ada'
                    else:
                        kondisi = 'Ada'
                elif c == 'disabilitas' :
                    if kondisi == 'Tidak disabilitas' :
                        kondisi = 'Tidak disabilitas'
                    else:
                        kondisi = 'Disabilitas'
                elif c == 'status_bangunan' :
                    if kondisi == 'Milik sendiri' :
                        kondisi = 'Milik sendiri'
                    elif kondisi == 'Kontrak/sewa' :
                        kondisi = 'Kontrak/sewa'
                    else:
                        kondisi = 'Bebas sewa'
                # print(f"kondisi: {kondisi}, k: {k}, get_bansos: {get_bansos}")
                bobot = str(Crips.objects.get(nama_crips=kondisi,kriteria=k,bansos=get_bansos).bobot_crips)
                bobot_kriteria = Kriteria.objects.get(nama_kriteria=c,bansos=get_bansos,tahun=tahun).bobot
                value = kondisi
                new = value.replace(value, str(bobot))
                data_kriteria.update({c:new})
                
                atribut = Kriteria.objects.get(nama_kriteria=c,bansos=get_bansos,tahun=tahun).atribut
                if bobot != None:
                    # MAX = max(new)
                    # MIN = min(new)
                    MAX = max(Crips.objects.values_list('bobot_crips', flat=True).filter(kriteria=k).filter(bansos=get_bansos))
                    MIN = min(Crips.objects.values_list('bobot_crips', flat=True).filter(kriteria=k).filter(bansos=get_bansos))
                    if atribut == "Benefit":
                        norm = int(new)/MAX
                        normr=round(norm,2)
                        data_kriteria1.update({c:normr})
                        nilai = norm*bobot_kriteria/100
                        nilair=round(nilai,2)
                        data_hitung.update({c:nilair})
                        nilai_akhir.append(nilair)
                    elif atribut == "Cost":
                        norm = MIN/int(new)
                        normr=round(norm,2)
                        data_kriteria1.update({c:normr})
                        nilai = norm*bobot_kriteria/100
                        nilair=round(nilai,2)
                        data_hitung.update({c:nilair})
                        nilai_akhir.append(nilair)
            # data_hitung.update({'nilai_akhir':sum(nilai_akhir)})
            data_hitung.update({'nilai_akhir': round(sum(nilai_akhir), 2)})
            data_hasil.append(data_hitung)
            data_hasil_sorted = sorted(data_hasil, key=lambda x: x['nilai_akhir'], reverse=True)
            # data_hasil_sorted_count = data_hasil_sorted.count()
            # print(data_hasil_sorted_count)
        cek_ranking = Ranking.objects.filter(bansos=get_bansos, tahun=tahun)
        # cek_ranking_count = Ranking.objects.filter(bansos=get_bansos, tahun=tahun).count()
        if cek_ranking:
            for s in data_hasil_sorted:
                id = s.get('id')
                hasil=s.get('nilai_akhir')
                anggota = Anggota.objects.get(id=id)
                update_ranking=Ranking.objects.filter(bansos__slug=slug, tahun=tahun).get(anggota=anggota)
                update_ranking.nilai=hasil
                update_ranking.save()
    # if not cek_ranking:        
    #     for d in data_hasil:
    #         nama = d.get('nama_art')
    #         id = d.get('id')
    #         anggota = Anggota.objects.get(id=id)
    #         hasil = d.get('nilai_akhir')
    #         data_ranking=Ranking(anggota = anggota,
    #                             status="Diranking",
    #                             tahun=tahun,
    #                             bansos=get_bansos,
    #                             alasan="",
    #                             nilai=hasil)
    #         data_ranking.save()
    t = []
            
    for year in daterange(2021, datetime.now().year):
        t.append(year)
    dihitung = Ranking.objects.filter(bansos__slug=slug, tahun = tahun, nilai__gt=0).count()
    diranking = Ranking.objects.filter(bansos__slug=slug).filter(tahun=tahun).filter(status='Diranking').count()
    context = {
        'bansos':bansos,
        'slug' : slug,
        'tahun' : tahun,
        'penerima':penerima,
        'kriteria':kriteria,
        'nama_kriteria':nama_kriteria,
        'data_crips' : data_crips,
        'data_normalisasi':data_normalisasi,
        'data_normalisasi1':data_normalisasi1,
        'data_hasil':data_hasil_sorted,
        'get_kriteria':get_kriteria,
        'title':'Perankingan',
        't' : t,
        'diranking':diranking,
        'dihitung':dihitung
    }
    return render(request, 'ranking/index.html', context) 

def delete_kriteria(request,slug,id,tahun):
    Kriteria.objects.get(bansos__slug=slug,tahun=tahun,id=id).delete()
    return redirect ('ranking:index',slug=slug, tahun = tahun)

def update_kriteria(request,slug,id,tahun):
    data_kriteria = Kriteria.objects.get(bansos__slug=slug,tahun=tahun,id=id)
    if request.method == "POST":
        data_kriteria.bobot = request.POST['bobot']
        data_kriteria.atribut = request.POST['atribut']
        data_kriteria.save()
    return redirect ('ranking:index',slug=slug, tahun = tahun)

def edit_bobot(request,slug,id,tahun):
    data_crips = Crips.objects.filter(kriteria=id)
    # print (data_crips)
    if request.method == "POST":
        for c in data_crips:
            c.bobot_crips = request.POST['bobot_'+c.nama_crips]
            c.save()
    return redirect ('ranking:index',slug=slug, tahun = tahun)

def simpan_ranking(request,slug,tahun):
    ranking = Ranking.objects.filter(bansos__slug=slug, tahun=tahun, status='Diranking')
    for s in ranking:
        s.status='Belum Diverifikasi'
        s.save()
    return redirect ('ranking:index', slug=slug, tahun=tahun)

def delete_ranking(request, slug, tahun):
    ranking = Ranking.objects.filter(bansos__slug=slug, tahun=tahun)
    for r in ranking:
        r.delete()
    kriteria = Kriteria.objects.filter(bansos__slug=slug, tahun=tahun)
    for k in kriteria:
        k.delete()
    return redirect('ranking:index', slug=slug, tahun=tahun)

status_bangunan = ['Milik sendiri', 'Kontrak/sewa', 'Bebas sewa']
luas_bangunan = ['>100 m2', '76-100 m2', '50-75 m2', '<50 m2']
# luas_bangunan = ['<50 m2', '50-75 m2', '76-100 m2', '>100 m2']
status_lahan = ['Milik sendiri', 'Dinas', 'Kontrak/sewa', 'Bebas sewa', 'Lainnya']
luas_lahan = ['<9 m2', '9-13 m2', '14-17 m2', '18-25 m2', '>25 m2']
luas_lantai = ['<8 m2', '8-12 m2', '13-16 m2', '17-24 m2', '>24 m2']
jenis_lantai = ['Kramik', 'Parkel/vinil/karpet', 'Ubin/tegel/teraso', 'Semen/bata merah', 'Tanah']
# jenis_lantai = ['Tanah', 'Semen/bata merah', 'Ubin/tegel/teraso', 'Kramik', 'Marmer/Granit']
jenis_dinding = ['Tembok', 'Plesteran anyaman bambu/kawat', 'Kayu/papan/gipsum/grc/kalcibot', 'Batang kayu', 'Bambu']
# jenis_dinding = ['Bambu','Batang kayu', 'Plesteran anyaman bambu', 'Kayu/papan/gipsum/grc/kalcibot', 'Tembok']
kondisi_dinding = ['Bagus / Kualitas Tinggi', 'Jelek / Kualitas rendah']
jenis_atap = ['Genteng tanah liat', 'Asbes', 'Seng', 'Sirap', 'Bambu']
# jenis_atap = ['Bambu', 'Sirap', 'Seng', 'Asbes', 'Genteng tanah liat']
kondisi_atap = ['Bagus / Kualitas Tinggi', 'Jelek / Kualitas rendah']
sumber_air = ['Air kemasan bermerk', 'Air isi ulang', 'ledeng meteran', 'ledeng eceran', 'Sumur bor/pompa', 'Sumur terlindung', 'Sumur tak terlindung', 'Mata air  terlindung', 'Mata air tak terlindung', 'Air sungai/danau/waduk', 'Air Hujan', 'Lainnya']
cara_air = ['Membeli eceran', 'Langganan', 'Tidak membeli']
sumber_penerangan = ['Listrik PLN', 'Listrik NON PLN', 'Bukan Listrik']
# sumber_penerangan = ['Bukan Listrik', 'Listrik NON PLN', 'Listrik PLN']
daya = ['450 watt', '900 watt', '1300 watt', '2200 watt', '>2200 watt', 'Tanpa Meteran']
status_listrik = ['Milik Sendiri', 'Menumpang tetangga']
bahan_bakar = ['Listrik', 'Gas > 3 kg', 'Gas 3kg', 'Gas kota / bio gas', 'minyak tanah', 'Briket', 'Arang', 'kayu bakar', 'Lainnya']
fasilitas_bab = ['Sendiri', 'Bersama', 'Umum', 'Tidak']
jenis_kloset = ['Leher Angsa', 'Plengsengan', 'Cumplung / cubluk', 'Tidak Pakai']
buang_tinja = ['Tangki', 'SPAR ( Saluran pembungan air limbah )', 'Lubang Tanah', 'Kolam/sawah / sungai/ danau / laut', 'Pantai / tanah lapang / kebun', 'lainnya']
bansos_pusat = ['RTLH', 'Air Bersih', 'Listrik', 'Jamban']
# bansos_provinsi = ['RTLH', 'Air Bersih', 'Listrik', 'Jamban']
# bansos_kota = ['RTLH', 'Air Bersih', 'Listrik', 'Jamban']
# bansos_desa = ['RTLH', 'Air Bersih', 'Listrik', 'Jamban']
# bansos_lainnya = ['RTLH', 'Air Bersih', 'Listrik', 'Jamban']

pengeluaran = ['0 - 400K', '400K -800K', '800K - 1200K', '1200K - 1600K', '1600K - 2000K']
penghasilan = ['0 - 400K', '400K -800K', '800K - 1200K', '1200K - 1600K', '1600K - 2000K', '> 2000K']
hubungan_krt = ['Kepala Rumah Tangga', 'Istri / suami', 'Anak', 'Menantu', 'Cucu', 'Orang tua / mertua', 'Pembantu / sopir', 'Lainnya']
hubungan_kk = ['Kepala keluarga', 'Istri / suami', 'Anak', 'Menantu', 'Cucu', 'Orang tua / mertua', 'Pembantu / sopir', 'Lainnya']
jenis_kelamin = ['Perempuan', 'Laki-Laki']
tanggal_lahir = ['>=65', '<65']
usia = ['<65', '>=65']
status_perkawinan = ['Belum kawin', 'Kawin / nikah', 'Cerai hidup', 'Cerai mati']
akta_nikah = ['Tidak', 'Ya, dapat ditunjukkan', 'Ya, tidak dapat ditunjukkan']
tercantum_kk = ['Ya', 'Tidak']
kepemilikan_kartu = ['Tidak Memiliki', 'Akta Kelahiran', 'Kartu Pelajar', 'KTP', 'SIM']
status_kehamilan = ['Ya', 'Tidak']
# sekolah = ['Masih sekolah', 'Tidak / belum sekolah', 'Tidak sekolah lagi']
sekolah = ['Masih sekolah', 'Tidak sekolah']
jenis_disabilitas = ['Tidak disabilitas', 'Disabilitas']
disabilitas = ['Tidak disabilitas', 'Disabilitas']
penyakit = ['Tidak ada', 'Ada']
jenjang_pendidikan = ['Tidak sekolah', 'SD / SDLB', 'Paket A', 'M. Ibtidiyah', 'ULA ( Pesantren setara SD )', 'SMP / SMPLB', 'Paket B', 'M. Tsanawiyah', 'Wustha ( Pesantren setara SMP )', 'SMA / SMK / SMALB', 'Paket C', 'M. Aliyah', 'Ulya ( Pesantren setra SMA )', 'Perguruan Tinggi']
status_bekerja = ['Bekerja', 'Tidak Bekerja']
status_kedudukan_kerja = ['Tidak bekerja', 'Berusaha sendiri', 'Berusaha dibantu buruh tidak tetap / tidak dibayar', 'Berusaha dibantu buruh tetap / dibayar', 'Buruh / Karyawan / Pegawai swasta', 'PNS / TNI / POLRI / BUMN / BUMD / Anggota Legislatif', 'Pekerja bebas pertanian', 'Pekerja bebas Non Pertanian', 'Pekerja keluarga / tidak dibayar']
bansos_provinsi = ['KJS', 'KUBE', 'PBI Pemda Provinsi']
bansos_kota = ['PBI Kab Kota', 'Lainnya']
bansos_desa = ['Dana Desa', 'Lainnya']
bansos_lainnya =['KUR', 'BPJS Mandiri', 'Asuransi kesehatan', 'BPJS Ketenagakerjaan', 'BPJS PPU', 'Lainnya']


