# Generated by Django 2.2 on 2020-07-22 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cookbook', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='name',
            field=models.CharField(max_length=128, unique=True),
        ),
    ]