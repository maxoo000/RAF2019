# Generated by Django 2.1.2 on 2018-12-20 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('korisnici', '0022_auto_20181220_1440'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clanovi',
            name='grad',
            field=models.CharField(choices=[('Nije naveden grad', 'Nije naveden grad'), ('Beograd', 'Beograd'), ('Valjevo', 'Valjevo'), ('Vranje', 'Vranje'), ('Zaječar', 'Zaječar'), ('Zrenjanin', 'Zrenjanin'), ('Jagodina', 'Jagodina'), ('Kragujevac', 'Kragujevac'), ('Kraljevo', 'Kraljevo'), ('Kruševac', 'Kruševac'), ('Leskovac', 'Leskovac'), ('Loznica', 'Loznica'), ('Niš', 'Niš'), ('Novi Pazar', 'Novi Pazar'), ('Novi Sad', 'Novi Sad'), ('Pančevo', 'Pančevo'), ('Požarevac', 'Požarevac'), ('Priština', 'Priština'), ('Smederevo', 'Smederevo'), ('Sombor', 'Sombor'), ('Sremska Mitrovica', 'Sremska Mitrovica'), ('Subotica', 'Subotica'), ('Užice', 'Užice'), ('Čačak', 'Čačak'), ('Šabac', 'Šabac'), ('Pirot', 'Pirot')], default='Nije naveden grad', max_length=254),
        ),
    ]
