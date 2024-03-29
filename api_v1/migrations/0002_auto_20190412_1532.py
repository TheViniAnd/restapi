# Generated by Django 2.1.3 on 2019-04-12 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_v1', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chargeutilitybills',
            name='TBO',
            field=models.FloatField(verbose_name='Вызов ТБО'),
        ),
        migrations.AlterField(
            model_name='chargeutilitybills',
            name='cold_weat',
            field=models.FloatField(verbose_name='Холодное водоснобжение'),
        ),
        migrations.AlterField(
            model_name='chargeutilitybills',
            name='elect_s',
            field=models.FloatField(verbose_name='Электроснабжение'),
        ),
        migrations.AlterField(
            model_name='chargeutilitybills',
            name='hot_weat',
            field=models.FloatField(verbose_name='Подогрев воды'),
        ),
        migrations.AlterField(
            model_name='chargeutilitybills',
            name='otoplen',
            field=models.FloatField(verbose_name='Отопление'),
        ),
        migrations.AlterField(
            model_name='chargeutilitybills',
            name='uborka',
            field=models.FloatField(verbose_name='Уборка с места общего пользования'),
        ),
    ]
