# Generated by Django 2.1.2 on 2018-12-20 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dogadjaji', '0022_auto_20181220_1335'),
    ]

    operations = [
        migrations.AddField(
            model_name='dogadjaji',
            name='ima_igraca',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
