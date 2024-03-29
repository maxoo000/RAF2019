# Generated by Django 2.1.2 on 2018-12-22 19:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('korisnici', '0026_clanovi_firma'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dogadjaji', '0029_prijava_organizator'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ocenjivanje',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ocena', models.FloatField(default=0)),
                ('datum_ocenjivanja', models.DateField(default=django.utils.timezone.now)),
                ('koji_dogadjaj', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dogadjaji.Dogadjaji')),
                ('ocenio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('organizator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='korisnici.Clanovi')),
            ],
        ),
    ]
