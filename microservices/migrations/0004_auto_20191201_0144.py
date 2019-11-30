# Generated by Django 2.2.7 on 2019-11-30 22:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('microservices', '0003_auto_20191130_2252'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pair',
            options={'verbose_name': 'Пара', 'verbose_name_plural': 'Пары'},
        ),
        migrations.AlterUniqueTogether(
            name='pair',
            unique_together={('first_microservice', 'second_microservice')},
        ),
    ]
