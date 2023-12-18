from django.contrib import admin
from .models import Penerima, Ranking

# Register your models here.
class PenerimaAdmin(admin.ModelAdmin):
    list_display = ('anggota', 'bansos', 'tahun')
class RankingAdmin(admin.ModelAdmin):
    list_display = ('anggota', 'bansos', 'tahun', 'status')
    

admin.site.register(Penerima, PenerimaAdmin)
admin.site.register(Ranking, RankingAdmin)
