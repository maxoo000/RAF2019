# Generated by Django 2.1.2 on 2018-12-20 14:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dogadjaji', '0027_auto_20181220_1443'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prijava',
            name='prijava_za_dogadjaj',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dogadjaji.Dogadjaji'),
        ),
    ]
