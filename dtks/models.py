from django.db import models
import geocoder
from django.template.defaultfilters import slugify

class Rumah(models.Model):
  IDJTG = models.CharField(max_length=255)
  nama_krt = models.CharField(max_length=100)
  kabupaten = models.CharField(max_length=100)
  kecamatan = models.ForeignKey("Kecamatan", on_delete=models.CASCADE)
  desa = models.CharField(max_length=100)
  dusun = models.CharField(max_length=100)
  rt = models.IntegerField()
  rw = models.IntegerField()
  alamat = models.CharField(max_length=150)
  koordinat_lat = models.CharField(max_length=100, null=True, blank=True)
  koordinat_long = models.CharField(max_length=100, null=True, blank=True)
  jum_anggota = models.IntegerField(default=0)
  
  def save(self, *args, **kwargs):
    if self.koordinat_lat is None and self.koordinat_long is None:  
      location = geocoder.osm(self.desa+" "+self.kabupaten)
      self.koordinat_lat = location.lat
      self.koordinat_long = location.lng
    super(Rumah, self).save(*args, **kwargs)

  def __str__(self) :
    return "{}".format(self.nama_krt)
  
class Kecamatan(models.Model):
  nama_kecamatan = models.CharField(max_length=100)
  class Meta: 
    ordering = ['nama_kecamatan']
  def __str__(self):
    return "{}".format(self.nama_kecamatan)

class Aset(models.Model):
  rumah = models.ForeignKey("Rumah", on_delete=models.CASCADE)
  gas = models.IntegerField(null=True, default=0)
  kulkas = models.IntegerField(null=True, default=0)
  ac = models.IntegerField(null=True, default=0)
  pemanas_air = models.IntegerField(null=True, default=0)
  telepon_rumah = models.IntegerField(null=True, default=0)
  tv = models.IntegerField(null=True, default=0)
  perhiasan = models.IntegerField(null=True, default=0)
  komputer = models.IntegerField(null=True, default=0)
  sepeda = models.IntegerField(null=True, default=0)
  motor = models.IntegerField(null=True, default=0)
  mobil = models.IntegerField(null=True, default=0)
  perahu = models.IntegerField(null=True, default=0)
  motor_tempel = models.IntegerField(null=True, default=0)
  perahu_motor = models.IntegerField(null=True, default=0)
  kapal = models.IntegerField(null=True, default=0)
  lahan = models.IntegerField(null=True, default=0)
  rumah_lain = models.IntegerField(null=True, default=0)
  sapi = models.IntegerField()
  kerbau = models.IntegerField()
  kuda = models.IntegerField()
  babi = models.IntegerField()
  kambing = models.IntegerField()
  unggas = models.IntegerField()
  pengeluaran = models.CharField(max_length=150)
  
  class Meta:
    ordering = ['pengeluaran']
  def __str__(self) :
    return "{}".format(self.rumah.nama_krt)
  
class Kondisi_Rumah(models.Model):
  rumah = models.ForeignKey("Rumah", on_delete=models.CASCADE)
  status_bangunan = models.CharField(max_length=100)
  luas_bangunan = models.IntegerField()
  status_lahan = models.CharField(max_length=100)
  luas_lahan = models.IntegerField()
  luas_lantai = models.IntegerField()
  jenis_lantai = models.CharField(max_length=100)
  jenis_dinding = models.CharField(max_length=100)
  kondisi_dinding = models.CharField(max_length=100)
  jenis_atap = models.CharField(max_length=100)
  kondisi_atap = models.CharField(max_length=100)
  jum_kamar = models.IntegerField()
  sumber_air = models.CharField(max_length=100)
  cara_air = models.CharField(max_length=100)
  sumber_penerangan = models.CharField(max_length=100)
  daya = models.CharField(max_length=100)
  id_pel = models.CharField(max_length=150, null=True)
  status_listrik = models.CharField(max_length=100)
  bahan_bakar = models.CharField(max_length=100)
  fasilitas_bab = models.CharField(max_length=100)
  jenis_kloset = models.CharField(max_length=100)
  buang_tinja = models.CharField(max_length=100)
  bansos_pusat = models.CharField(max_length=100, null=True)
  bansos_provinsi = models.CharField(max_length=100, null=True)
  bansos_kota = models.CharField(max_length=100, null=True)
  bansos_desa = models.CharField(max_length=100, null=True)
  bansos_lainnya = models.CharField(max_length=100, null=True)
  sumber_bansos = models.CharField(max_length=100, null=True)
  koordinat_lat = models.CharField(max_length=100, null=True, blank=True)
  koordinat_long = models.CharField(max_length=100, null=True, blank=True)
  class Meta:
    ordering = ['luas_lahan']
  def __str__(self) :
    return "{}".format(self.rumah.nama_krt)
  
  @classmethod
  def fields(self):
    return [f.name for f in self._meta.fields]
  
class Anggota(models.Model):
  IDJTG_ART = models.CharField(max_length=20)
  rumah = models.ForeignKey("Rumah", on_delete=models.CASCADE)
  nama_art = models.CharField(max_length=255)
  nik = models.CharField(max_length=16, unique = True)
  no_kk = models.CharField(max_length=100)
  ibu_kandung = models.CharField(max_length=255)
  hubungan_krt = models.CharField(max_length=100)
  hubungan_kk = models.CharField(max_length=100)
  tempat_lahir = models.CharField(max_length=100)
  tanggal_lahir = models.DateField()
  jenis_kelamin = models.CharField(max_length=50)
  status_perkawinan = models.CharField(max_length=100)
  akta_nikah = models.CharField(max_length=100)
  tercantum_kk = models.CharField(max_length=100)
  kepemilikan_kartu = models.CharField(max_length=100)
  status_kehamilan = models.CharField(max_length=100)
  tgl_kehamilan = models.CharField(max_length=100, null=True)
  jenis_disabilitas = models.CharField(max_length=100)
  penyakit = models.CharField(max_length=100)
  sekolah = models.CharField(max_length=100)
  jenjang_pendidikan = models.CharField(max_length=100, null=True, default="Tidak sekolah")
  kelas_tertinggi = models.CharField(max_length=100, null=True, default=0)
  ijazah_tertinggi = models.CharField(max_length=100, null=True, default="Tidak punya ijazah")
  status_bekerja = models.CharField(max_length=100, null=True, default="Tidak Bekerja")
  lapangan_usaha = models.CharField(max_length=100, null=True, default="Tidak bekerja")
  status_kedudukan_kerja = models.CharField(max_length=100, null=True, default="Tidak bekerja")
  jenis_ketrampilan = models.CharField(max_length=100, null=True, default="Tidak Ada")
  bansos_pusat = models.CharField(max_length=100, null=True)
  bansos_provinsi = models.CharField(max_length=100, null=True)
  bansos_kota = models.CharField(max_length=100, null=True)
  bansos_desa = models.CharField(max_length=100, null=True)
  bansos_lainnya = models.CharField(max_length=100, null=True)
  
  class Meta:
    ordering = ['nama_art']
  def __str__(self) :
    return "{}".format(self.nama_art)
  
class Bansos(models.Model):
  nama_bansos = models.CharField(max_length=50)
  color = models.CharField(max_length=50, blank=True, null=True)
  kuota = models.CharField(max_length=50, blank=True, null=True)
  slug = models.SlugField(default="", null=True, blank=True)

  def save(self, *args, **kwargs):
        self.slug = slugify(self.nama_bansos)
        super(Bansos, self).save(*args, **kwargs)
  def __str__(self):
    return "{}".format(self.nama_bansos)
