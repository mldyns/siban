# Generated by Django 4.2.1 on 2023-09-18 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Jenis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama_cluster', models.CharField(max_length=100)),
                ('jumlah_k', models.IntegerField()),
                ('atribut', models.CharField(max_length=100)),
            ],
        ),
    ]
