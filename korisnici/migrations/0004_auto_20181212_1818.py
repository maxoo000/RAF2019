# Generated by Django 2.1.2 on 2018-12-12 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('korisnici', '0003_clanovi_broj_telefona'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clanovi',
            name='omiljeni_sport',
            field=models.CharField(choices=[('Nije dodato', 'Nije dodato'), ('Fudbal', 'Fudbal'), ('Kosarka', 'Kosarka'), ('Tenis', 'Tenis'), ('Odbojka', 'Odbojka')], default='Nije dodato', max_length=254),
        ),
    ]
