# Generated by Django 2.1.2 on 2018-12-20 02:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dogadjaji', '0017_auto_20181218_0541'),
    ]

    operations = [
        migrations.AddField(
            model_name='dogadjaji',
            name='asport',
            field=models.CharField(choices=[('Fudbal', 'Fudbal'), ('Kosarka', 'Kosarka'), ('Tenis', 'Tenis'), ('Odbojka', 'Odbojka')], default='Fudbal', max_length=254),
        ),
    ]
