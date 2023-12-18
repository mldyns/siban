from django.contrib import admin
from .models import Rumah, Aset, Kondisi_Rumah, Anggota, Bansos, Kecamatan

admin.site.register(Rumah)
admin.site.register(Kecamatan)
admin.site.register(Aset)
admin.site.register(Kondisi_Rumah)
admin.site.register(Anggota)
admin.site.register(Bansos)