# Generated by Django 4.2.1 on 2023-11-17 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('penerima', '0002_alter_ranking_nilai'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ranking',
            name='nilai',
            field=models.DecimalField(blank=True, decimal_places=2, default='0', max_digits=3, null=True),
        ),
    ]
