# Generated by Django 2.1.2 on 2018-12-12 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('korisnici', '0005_auto_20181212_1835'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clanovi',
            name='pol',
            field=models.CharField(choices=[('Musko', 'Musko'), ('Zensko', 'Zensko'), ('/', '/')], default='/', max_length=5),
        ),
    ]
