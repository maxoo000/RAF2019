# Generated by Django 2.1.2 on 2018-12-15 01:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('korisnici', '0013_clanovi_opis'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clanovi',
            name='pol',
            field=models.CharField(choices=[('Musko', 'Musko'), ('Zensko', 'Zensko'), ('Ne bih da navodim', 'Ne bih da navodim')], default='/', max_length=5),
        ),
    ]
