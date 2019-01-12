# Generated by Django 2.1.2 on 2018-12-16 22:23

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('dogadjaji', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dogadjaj',
            name='mesto',
            field=models.CharField(default='Nije oznaceno', max_length=150),
        ),
        migrations.AlterField(
            model_name='dogadjaj',
            name='datum_kreiranja',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='dogadjaj',
            name='datum_odrzavanja',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]