# Generated by Django 2.1.2 on 2018-12-15 03:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('korisnici', '0016_auto_20181215_0422'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clanovi',
            name='grad',
            field=models.CharField(choices=[('Nije naveden grad', 'Nije naveden grad'), ('Beograd', 'Beograd'), ('Cacak', 'Cacak'), ('Uzice', 'Uzice'), ('Ivanjica', 'Ivanjica'), ('Novi sad', 'Novi sad'), ('Nis', 'Nis'), ('Pozega', 'Pozega'), ('Lucani', 'Lucani')], default='Nije naveden grad', max_length=254),
        ),
    ]