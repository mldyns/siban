from import_export import resources
from penerima.models import Penerima
from dtks.models import Anggota, Bansos
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget

class PenerimaResource(resources.ModelResource):
    id = Field(
        column_name='ID',
        attribute='id',)
    anggota = Field(
        column_name='ANGGOTA',
        attribute='anggota',
        widget=ForeignKeyWidget(model=Anggota, field='nama_art'))
    bansos = Field(
        column_name='BANSOS',
        attribute='bansos',
        widget=ForeignKeyWidget(model=Bansos, field='nama_bansos'))
    tahun = Field(
        column_name='TAHUN',
        attribute='tahun',)
    status = Field(
        column_name='STATUS',
        attribute='status',)
    class Meta:
        model = Penerima
        fields = ('id', 'anggota', 'bansos', 'tahun', 'status')