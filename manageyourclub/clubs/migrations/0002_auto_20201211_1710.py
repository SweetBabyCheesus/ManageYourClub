# Generated by Django 2.2.6 on 2020-12-11 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addressmodel',
            name='houseNumber',
            field=models.CharField(max_length=5),
        ),
    ]