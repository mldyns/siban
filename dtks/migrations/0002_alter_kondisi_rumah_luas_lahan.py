# Generated by Django 4.2.1 on 2023-11-02 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dtks', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kondisi_rumah',
            name='luas_lahan',
            field=models.CharField(max_length=100),
        ),
    ]
