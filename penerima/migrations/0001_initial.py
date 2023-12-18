# Generated by Django 4.2.1 on 2023-09-18 19:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('dtks', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ranking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Belum Diverifikasi', 'Belum Diverifikasi'), ('Disetujui', 'Disetujui'), ('Ditolak', 'Ditolak'), ('Penerima', 'Penerima')], default='Belum Diverifikasi', max_length=20)),
                ('tahun', models.CharField(blank=True, max_length=10, null=True)),
                ('alasan', models.CharField(blank=True, max_length=200, null=True)),
                ('nilai', models.FloatField(blank=True, default='0', null=True)),
                ('anggota', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dtks.anggota')),
                ('bansos', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dtks.bansos')),
            ],
        ),
        migrations.CreateModel(
            name='Penerima',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('foto_bukti', models.FileField(null=True, upload_to='bukti/')),
                ('tahun', models.CharField(blank=True, max_length=10, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('Dalam Proses', 'Dalam Proses'), ('Diterima', 'Diterima')], default='Dalam Proses', max_length=60)),
                ('anggota', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dtks.anggota')),
                ('bansos', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dtks.bansos')),
            ],
        ),
    ]
