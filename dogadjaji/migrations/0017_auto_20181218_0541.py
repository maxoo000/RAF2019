# Generated by Django 2.1.2 on 2018-12-18 04:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dogadjaji', '0016_auto_20181217_0352'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prijava',
            name='prijavu_poslao',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
