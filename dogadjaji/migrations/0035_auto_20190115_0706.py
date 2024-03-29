# Generated by Django 2.1.2 on 2019-01-15 06:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('korisnici', '0026_clanovi_firma'),
        ('dogadjaji', '0034_maxo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Poziv',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Prihvaceno', 'Prihvaceno'), ('Odbijeno', 'Odbijeno'), ('Ceka se odgovor', 'Ceka se odgovor')], default='Ceka se odgovor', max_length=100)),
                ('ko_je_pozvan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='korisnici.Clanovi')),
                ('koji_dogadjaj', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dogadjaji.Dogadjaji')),
                ('pozvao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='maxo',
        ),
    ]
