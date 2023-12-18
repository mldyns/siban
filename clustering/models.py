from django.db import models
from dtks.models import Rumah 

class Jenis(models.Model):
  nama_cluster = models.CharField(max_length=100)
  jumlah_k = models.IntegerField()
  atribut = models.CharField(max_length=100)

  def __str__(self):
    return "{}".format(self.nama_cluster)
  